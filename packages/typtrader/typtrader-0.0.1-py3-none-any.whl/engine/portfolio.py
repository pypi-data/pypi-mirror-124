import os
import json
import time
import redis
import datetime
from copy import deepcopy
from decimal import Decimal
from typing import Dict, List
from flatten_dict import flatten
from multiprocessing import Queue
from collections import OrderedDict

from engine.events import (
    SignalEvent,
    PairSignalEvent,
    OrderEvent,
    PairOrderEvent,
    OrderSuccessEvent,
    FillEvent,
    JangoEvent,
)
from engine.utils.log import Logger, CoinTelegram
from engine.utils.distributed_queue import DistributedQueue

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
application = get_wsgi_application()

# from db.models import PairSignal_Table, Order_Table, Fill_Table, Signal_Table
from params import (
    EXCHANGE_LIST,
    EXECUTION_QUEUE_HOST,
    EXECUTION_QUEUE_PORT,
    STRATEGY_QUEUE_HOST,
    EXAMPLE_STRATEGY_QUEUE_PORT,
    LOG_QUEUE_HOST,
    LOG_QUEUE_PORT,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PASSWORD,
)

STRATEGY_LS = ['example']

STRATEGY_PORTS = {
    'example': EXAMPLE_STRATEGY_QUEUE_PORT,
}


class Portfolio:
    """
    Portfolio의 역할

    1. 원장 관리
      - Order 나오면 원장에 등록 후 Exec으로 보내기 -> 추후 AH를 통해 FillEvent 받아 Port Update 수행
      - Exec에서는 원장 정보에 대해 상시 요청 및 수정(Status 바꿔주기)이 가능해야 한다 (Order 정보도 DB에 등록)

    2. 현재 보유 Positions 및 Holdings 관리
      - FillEvent를 받으면 Current Positions와 Holdings를 업데이트 함
      - 일정 주기별로 현재 가격을 받아 Holdings를 업데이트하고 DB로 전송 (Time Cost가 있음으로 따로 분리할지 고려 필요,
                                                             확장성을 위해 Array 방식 사용 필수)
    """

    def __init__(self,
                 execution_host: str = EXECUTION_QUEUE_HOST,
                 execution_port: int = EXECUTION_QUEUE_PORT,
                 execution_queue: Queue = None,
                 strategy_host: str = STRATEGY_QUEUE_HOST,
                 strategy_ports: Dict[str, int] = STRATEGY_PORTS,
                 strategy_queues: Dict[str, Queue] = None,
                 log_host: str = LOG_QUEUE_HOST,
                 log_port: int = LOG_QUEUE_PORT,
                 redis_host: str = REDIS_HOST,
                 redis_port: int = REDIS_PORT,
                 redis_password: str = REDIS_PASSWORD,
                 strategy_ls: List[str] = STRATEGY_LS,
                 backtest: bool = False,
                 debug: bool = False):

        self.debug = debug
        self.backtest = backtest

        if execution_queue is None:
            self.execution_queue = DistributedQueue(execution_port, execution_host)
            print(f'[Portfolio] Created Execution DistributedQueue at tcp://{execution_host}:{execution_port}')
        else:
            self.execution_queue = execution_queue

        if strategy_queues is None:
            self.strategy_queues = {st: DistributedQueue(st_port, strategy_host)
                                    for st, st_port in strategy_ports.items()}
            print(f'[Portfolio] Created Strategy DistributedQueues')
        else:
            self.strategy_queues = strategy_queues

        self.logger = Logger(log_port, log_host, debug=self.debug)
        self.telegram = CoinTelegram(debug=self.debug)

        self.cnt = 0
        self.jango_cnt = 0
        self.jango_updated = False
        self.init_jango_sig = False
        self.today_str = datetime.datetime.now().strftime('%Y-%m-%d')

        self.strategy_ls: List[str] = strategy_ls
        self.order_table: Dict[str, OrderedDict] = {st: OrderedDict() for st in self.strategy_ls}

        # Positions만 있으면 Holdings를 구할수 있게 구현해야한다.
        self.current_positions = {}  # Account 에서 둘다 만들어서 jango event로 넘어온다.
        self.current_holdings = {}

        if not self.backtest:
            self.redis_conn = redis.StrictRedis(host=redis_host,
                                                port=redis_port,
                                                password=redis_password)

        self.spot_USDT_holdings = {}

    # Jango Event Update
    def update_jango(self, event: JangoEvent, method: str):
        """
        Updates Current Positions according to JangoEvent from HTS/Exchange.
        """
        if event.type == 'JANGO' and not self.init_jango_sig:
            self.current_positions = event.api_current_positions
            self.current_holdings = event.api_current_holdings

            # 장시작 업데이트된 초기 포지션 정보 Redis 업데이트.
            self.update_cur_position_to_redis()
            self.update_cur_holdings_to_redis()

            # Usdt 현금 초기 세팅
            for st in self.strategy_ls:
                for e in EXCHANGE_LIST:
                    self.spot_USDT_holdings[e] = self.current_holdings[st][e]['spot']['USDT']

            if method == 'request':
                self.init_jango_sig = False
            elif method == 'self_update':  # 프로그렘 시작시 잔고 한번 받아옴
                self.init_jango_sig = True

        elif event.type == 'JANGO' and self.init_jango_sig:
            pass

        else:
            self.logger.error('Wrong JANGO request @ Portfolio')

    # Redis update
    def update_cur_position_to_redis(self):
        # backtest 인 경우 메모리 공유됨으로 업데이트 해줄 필요없음
        if self.backtest:
            return

        s = time.time()
        for st in self.strategy_ls:
            pos_key = f'position_{st}'
            self.redis_conn.delete(pos_key)  # 업데이트전 전체 삭제, 과거 position 잔재 없에기

            flatten_pos = flatten(self.current_positions[st], reducer='underscore')

            # Pipeline need for bulk hset of Position Table!
            pipeline = self.redis_conn.pipeline()
            for k, v in flatten_pos.items():
                pipeline.hset(pos_key, k, v)
            pipeline.execute()

        self.logger.debug(f'[Portfolio] Update all Cur_Position to Redis took: {time.time() - s} sec.')

    def update_cur_holdings_to_redis(self):
        # backtest 인 경우 메모리 공유됨으로 업데이트 해줄 필요없음
        if self.backtest:
            return

        s = time.time()
        for st in self.strategy_ls:
            hold_key = f'holdings_{st}'
            self.redis_conn.delete(hold_key)  # 업데이트전 전체 삭제, 과거 position 잔재 없에기

            flatten_pos = flatten(self.current_holdings[st], reducer='underscore')

            # Pipeline need for bulk hset of Holdings Table!
            pipeline = self.redis_conn.pipeline()
            for k, v in flatten_pos.items():
                pipeline.hset(hold_key, k, v)
            pipeline.execute()

        self.logger.debug(f'[Portfolio] Update all Cur_Holdings to Redis took: {time.time() - s} sec.')

    def redis_position_getter(self,
                              strategy_id: str,
                              exchange: str,
                              asset_type: str,
                              symbol: str,
                              long_short: str,
                              p_q_lev: str):
        if self.backtest:
            res = self.current_positions[strategy_id][exchange][asset_type][symbol][long_short][p_q_lev]
        else:
            pos_key = f'position_{strategy_id}'
            pos_field = f'{exchange}_{asset_type}_{symbol}_{long_short}_{p_q_lev}'
            res = self.redis_conn.hget(pos_key, pos_field)
            res = json.loads(res)
        return res

    def redis_position_setter(self,
                              strategy_id: str,
                              exchange: str,
                              asset_type: str,
                              symbol: str,
                              long_short: str,
                              p_q_lev: str,
                              value: int or float):
        if self.backtest:
            self.current_positions[strategy_id][exchange][asset_type][symbol][long_short][p_q_lev] = value
        else:
            pos_key = f'position_{strategy_id}'
            pos_field = f'{exchange}_{asset_type}_{symbol}_{long_short}_{p_q_lev}'
            self.redis_conn.hset(pos_key, pos_field, value)

    def redis_holdings_setter(self,
                              strategy_id: str,
                              exchange: str,
                              asset_type: str,
                              symbol: str,
                              value: int or float):
        if self.backtest:
            self.current_holdings[strategy_id][exchange][asset_type][symbol] = value
        else:
            pos_key = f'holdings_{strategy_id}'
            pos_field = f'{exchange}_{asset_type}_{symbol}'
            self.redis_conn.hset(pos_key, pos_field, value)

    # Event DB update
    def update_signal_event_to_DB(self, evt: SignalEvent):
        if self.backtest:
            return

        s = time.time()
        evt.save()
        self.logger.debug(f'[Portfolio] Updating SignalEvent to DB took: {round(time.time() - s, 3)} sec.')

    def update_pairsignal_event_to_DB(self, evt: PairSignalEvent):
        if self.backtest:
            return

        s = time.time()
        evt.save()
        self.logger.debug(f'[Portfolio] Updating PairSignalEvent to DB took: {round(time.time() - s, 3)} sec.')

    def update_order_event_to_DB(self, evt: OrderEvent):
        if self.backtest:
            return

        if evt.type == "ORDER":
            s = time.time()
            if evt.direction == "ENTRY":
                # Threading event 객체 True, False 로 바꿔주기. DB 저장용
                evt.leverage_confirmed = evt.leverage_confirmed.is_set()
                evt.margin_type_confirmed = evt.margin_type_confirmed.is_set()
                evt.transfer_confirmed = evt.transfer_confirmed.is_set()
                evt.order_confirmed = evt.order_confirmed.is_set()
            elif evt.direction == "EXIT":
                evt.order_confirmed = evt.order_confirmed.is_set()
                evt.repay_confirmed = evt.repay_confirmed.is_set()
                evt.transfer_confirmed = evt.transfer_confirmed.is_set()

            o = Order_Table(**evt.__dict__)
            o.save()
            self.logger.debug(f"Updating OrderEvent to DB took: {round(time.time() - s, 3)} sec.")

    def update_fill_event_to_DB(self, evt: FillEvent):
        if self.backtest:
            return

        s = time.time()
        f = Fill_Table(**evt.__dict__)
        f.save()
        self.logger.debug(f"Updating FillEvent to DB took: {round(time.time() - s, 3)} sec.")

    # Fill Event Update
    def update_order_table_from_fill(self, evt: FillEvent):
        # strategy_id = evt.strategy_id # Matching 전이여서 None 값 나옴.

        # 1. Order Table Remaing_q 줄여주기 및 Status 변경
        updated = False
        order_status = None  # Fill Event가 Partial인지 Filled인지에 따라 OrderSuccess Event(Filled일때 발생)를 발생시키기 위해.

        for st in self.strategy_ls:
            for k, v in self.order_table[st].items():
                o = self.order_table[st][k]
                # print(f"print order table!!! @ PORT")
                # pprint(o.__dict__)

                # Fill Event에 Order Event 정보 업데이트.
                evt.direction = o.direction  # fill_event에 Direction 알려주기.
                evt.signal_uid = o.signal_uid  # fill_event에 signal_uid 넘겨주기. 추후 signal_uid로 signal, order, fill 모두 조회가능.
                evt.order_uid = o.order_uid  # fill_event에 order_uid 넘겨주기. order_uid를 기준으로 order_success event 발생.
                evt.strategy_id = o.strategy_id

                # order remaining 가감
                # 첫번째 order부터 차례대로 돈다. 앞 order 먼저 api_order_id 부여
                if o.api_order_uid is None:
                    if o.matcher == evt.matcher:
                        o.api_order_uid = evt.api_order_uid  # order_event에 api_order_id 넘겨줌. 현재 사용처 없음.
                        # Float 연산 시에는 Decimal 씌워줘야 정확히 0 값이 나올 수 있음.
                        o.remaining_quantity = Decimal(str(o.quantity)) - Decimal(
                            str(evt.filled_quantity))  # evt.order_quantity랑 비교하면 더 좋을지 생각해보기.

                        if o.remaining_quantity == 0:  # TODO :: 완벽하게 0이 될수없음. Commission 만큼의 오차는 허용해야 한다. 만약 마진 Sell 을 청산하는 경우라면 Repay 남는 금액까지 고려필요...
                            o.status = "FILLED"
                            order_status = "FILLED"
                        else:
                            o.status = "PARTIALLY_FILLED"
                            order_status = "PARTIALLY_FILLED"
                        updated = True
                        break
                else:
                    if o.api_order_uid == evt.api_order_uid:
                        o.remaining_quantity = Decimal(str(o.remaining_quantity)) - Decimal(str(evt.filled_quantity))

                        if o.remaining_quantity == 0:  # TODO :: 완벽하게 0이 될수없음. Commission 만큼의 오차는 허용해야 한다. 만약 마진 Sell 을 청산하는 경우라면 Repay 남는 금액까지 고려필요...
                            o.status = "FILLED"
                            order_status = "FILLED"
                        else:
                            o.status = "PARTIALLY_FILLED"
                            order_status = "PARTIALLY_FILLED"
                        updated = True
                        break

        # 2. 변경 내용 저장하기
        if not updated:
            self.logger.error(f"!!!! This FillEvent has no matching order: {evt.__dict__} !!!! @ Port")

        return order_status

    def update_positions_from_fill(self, evt: FillEvent):
        # TODO :: Position Update 후 Redis 업데이하는 부분 추가 필요.

        """
        Takes a Fill object and updates the position matrix to reflect the new position.
        :param fill: The Fill object to update the position with
        """
        strategy_id = evt.strategy_id
        exchange = evt.exchange
        asset_type = evt.asset_type
        log_time = evt.log_time
        symbol = evt.symbol
        filled_quantity = evt.filled_quantity
        side = evt.side
        fill_cost = evt.fill_cost
        est_fill_cost = evt.est_fill_cost
        commission = evt.commission
        direction = evt.direction

        # 0. 직전 Quantity와 Avg. Price 저장
        pos_q = None
        pos_p = None
        try:
            # API에서는 ENTRY LONG을 EXIT SHORT으로 청산함. 웹은 반대
            if direction == 'ENTRY':
                if side == 'BUY':
                    pos_q = deepcopy(self.current_positions[strategy_id][exchange][asset_type][symbol]['long']['q'])
                    pos_p = deepcopy(self.current_positions[strategy_id][exchange][asset_type][symbol]['long']['p'])
                elif side == 'SELL':
                    pos_q = deepcopy(self.current_positions[strategy_id][exchange][asset_type][symbol]['short']['q'])
                    pos_p = deepcopy(self.current_positions[strategy_id][exchange][asset_type][symbol]['short']['p'])

            elif direction == 'EXIT':
                if side == 'BUY':
                    pos_q = deepcopy(self.current_positions[strategy_id][exchange][asset_type][symbol]['short']['q'])
                    pos_p = deepcopy(self.current_positions[strategy_id][exchange][asset_type][symbol]['short']['p'])
                elif side == 'SELL':
                    pos_q = deepcopy(self.current_positions[strategy_id][exchange][asset_type][symbol]['long']['q'])
                    pos_p = deepcopy(self.current_positions[strategy_id][exchange][asset_type][symbol]['long']['p'])
            else:
                pos_q, pos_p = 0, 0
                # pos_l_q, pos_s_q, pos_l_p, pos_s_p = 0, 0, 0, 0

        except KeyError:  # 기존 position이 없는 불특정 종목이 들어올수는 없긴함.
            coin_logger.exception("기존 cur_position에 없는 불특정 종목이 들어옴!")
            pos_q, pos_p = None, None
            # pos_l_q, pos_s_q, pos_l_p, pos_s_p = 0, 0, 0, 0

        if pos_q < 0:
            self.logger.error(f"!!!!! position Quantity should not be Negative !!!! @ Port")

        # 1. Update Quantity
        if direction == 'ENTRY':
            updated_pos_q = float(Decimal(str(pos_q)) + Decimal(str(filled_quantity)))  # pos_q 도 abs 해줘야하는거 아닐까?
            l_s = 'long' if side == 'BUY' else 'short' if side == 'SELL' else None

            if asset_type == 'margin' and side == 'BUY':
                updated_pos_q = float(Decimal(str(pos_q)) + Decimal(str(filled_quantity)) - Decimal(str(commission)))

            # if symbol == "LINKUSDT" and asset_type == 'usdt':
            #     print(f"%%%%%%%%%%% {symbol}  q: {updated_pos_q}")

        elif direction == 'EXIT':
            updated_pos_q = float(Decimal(str(pos_q)) - Decimal(str(filled_quantity)))
            l_s = 'short' if side == 'BUY' else 'long' if side == 'SELL' else None

        else:
            updated_pos_q = None
            l_s = None
            self.logger.error(f"'Direction should be ENTRY or EXIT : {direction} @ Port")

        self.current_positions[strategy_id][exchange][asset_type][symbol][l_s]['q'] = updated_pos_q
        self.redis_position_setter(strategy_id=strategy_id,
                                   exchange=exchange,
                                   asset_type=asset_type,
                                   symbol=symbol,
                                   long_short=l_s,
                                   p_q_lev='q',
                                   value=updated_pos_q)

        # 2. Update Average Price
        # 전량 Exit 된 경우
        if updated_pos_q == 0:
            if side == 'BUY':
                for p_q_lev in ['p', 'q', 'leverage']:
                    self.current_positions[strategy_id][exchange][asset_type][symbol]['long'][p_q_lev] = 0
                    self.redis_position_setter(strategy_id=strategy_id,
                                               exchange=exchange,
                                               asset_type=asset_type,
                                               symbol=symbol,
                                               long_short='long',
                                               p_q_lev=p_q_lev,
                                               value=0)

            if side == 'SELL':
                for p_q_lev in ['p', 'q', 'leverage']:
                    self.current_positions[strategy_id][exchange][asset_type][symbol]['short'][p_q_lev] = 0
                    self.redis_position_setter(strategy_id=strategy_id,
                                               exchange=exchange,
                                               asset_type=asset_type,
                                               symbol=symbol,
                                               long_short='short',
                                               p_q_lev=p_q_lev,
                                               value=0)
        else:
            # 같은 포지션(long, short)으로 추가 entry or pos_q가 0일때(처음진입)
            if direction == 'ENTRY':
                # LONg
                if side == 'BUY':
                    self.current_positions[strategy_id][exchange][asset_type][symbol]['long']['p'] = ((
                                                                                                                  pos_q * pos_p) + fill_cost) / updated_pos_q
                    self.redis_position_setter(strategy_id=strategy_id,
                                               exchange=exchange,
                                               asset_type=asset_type,
                                               symbol=symbol,
                                               long_short='long',
                                               p_q_lev='p',
                                               value=((pos_q * pos_p) + fill_cost) / updated_pos_q)
                # SHORT
                elif side == 'SELL':
                    self.current_positions[strategy_id][exchange][asset_type][symbol]['short']['p'] = ((
                                                                                                                   pos_q * pos_p) + fill_cost) / updated_pos_q
                    self.redis_position_setter(strategy_id=strategy_id,
                                               exchange=exchange,
                                               asset_type=asset_type,
                                               symbol=symbol,
                                               long_short='short',
                                               p_q_lev='p',
                                               value=((pos_q * pos_p) + fill_cost) / updated_pos_q)

                # if symbol == "LINKUSDT" and asset_type == "usdt":
                #     print(
                #         f" %%%%%%%%%%%%%%% {symbol}  p: {self.current_positions[strategy_id][exchange][asset_type][symbol]['short']['p']}")

            # 같은 포지션에서 부분 exit
            # TODO 같은 값 넣을거면 필요없는 부분인듯
            elif direction == 'EXIT':
                if side == 'BUY':
                    self.current_positions[strategy_id][exchange][asset_type][symbol]['short']['p'] = pos_p
                    self.redis_position_setter(strategy_id=strategy_id,
                                               exchange=exchange,
                                               asset_type=asset_type,
                                               symbol=symbol,
                                               long_short='short',
                                               p_q_lev='p',
                                               value=pos_p)
                # SHORT
                elif side == 'SELL':
                    self.current_positions[strategy_id][exchange][asset_type][symbol]['long']['p'] = pos_p
                    self.redis_position_setter(strategy_id=strategy_id,
                                               exchange=exchange,
                                               asset_type=asset_type,
                                               symbol=symbol,
                                               long_short='long',
                                               p_q_lev='p',
                                               value=pos_p)

        # TODO : Position Redis Update 추가!!
        self.logger.info(f'체결 업데이트 완료: {self.current_positions[strategy_id][exchange][asset_type][symbol]} @ Portfolio')

    def update_holdings_from_fill(self, evt: FillEvent):
        """
        Takes a Fill object and updates the holding matrix to reflect the holdings value.
        :param fill: The Fill object to update the holdings with
        """

        strategy_id = evt.strategy_id
        exchange = evt.exchange
        asset_type = evt.asset_type
        log_time = evt.log_time
        symbol = evt.symbol
        filled_quantity = evt.filled_quantity
        side = evt.side
        fill_cost = evt.fill_cost
        est_fill_cost = evt.est_fill_cost
        commission = evt.commission
        direction = evt.direction

        fill_dir = -1 if direction == "ENTRY" else 1 if direction == "EXIT" else None

        # TODO : holdings의 spot usdt 만 업데이트해서 나머지 Symbol 들은 holdings tracker 에서 업데이트 한다음 log 함.
        # print(f'%%%%%%%%%%%% before spot_USDT_holdings : {self.spot_USDT_holdings[exchange]}')

        if direction == "ENTRY":
            l_s = 'long' if side == 'BUY' else 'short'
        elif direction == "EXIT":
            l_s = 'short' if side == 'BUY' else 'long'
        else:
            l_s = None

        lev = self.redis_position_getter(strategy_id=strategy_id,
                                         exchange=exchange,
                                         asset_type=asset_type,
                                         symbol=symbol,
                                         long_short=l_s,
                                         p_q_lev='leverage')
        lev = 1 if lev == 0 else lev

        self.spot_USDT_holdings[exchange] += (fill_dir/lev) * fill_cost  # TODO : Commission 반영 필요?
        # print(f'%%%%%%%%%%%% after spot_USDT_holdings : {self.spot_USDT_holdings[exchange]} , {fill_dir/lev * fill_cost}')

        self.redis_holdings_setter(strategy_id=strategy_id,
                                   exchange=exchange,
                                   asset_type='spot',
                                   symbol='USDT',
                                   value=self.spot_USDT_holdings[exchange])

        # # Check whether the fill is a buy or sell
        # # BUY / SELL (2가지만 가능!)
        # if side == 'BUY':
        #     fill_dir = 1
        # elif side == 'SELL':
        #     fill_dir = -1
        # else:
        #     raise Exception("Wrong fill.direction @ Portfolio")
        #
        # # Update holdings list with new quantity
        # # Live Trading 에서는 매입금액 사용하면 될듯, 결국 Slippage 비용도 여기에 반영해야함.
        # if exchange == 'binance' or exchange == 'bybit':
        #     fill_cost = fill_dir * fill_cost / leverage
        # else:
        #     fill_price = self.bar.get_latest_bar_value(exchange, asset_type, symbol, 'current_price')
        #     fill_cost = fill_dir * fill_price * evt.filled_quantity
        #
        # # TODO 태훈
        # # TODO :: Entry 인지 Exit 인지에 따라 fill_cost 반영 방식 다를듯...! 모든 fill에 대해 entry exit 구현?
        # self.current_holdings[strategy_id][exchange][asset_type][symbol] += fill_cost
        # self.current_holdings[strategy_id][exchange][asset_type]['commission'] += commission  # 수수료
        # self.current_holdings[strategy_id][exchange][asset_type]["USDT"] -= fill_cost + commission
        # # update_timeindex에서 q * current_price 된 평가금액 얹어줌. # 필요없는 부분인것 같기도..일부러 cash랑 맞춰줌
        # # self.current_holdings[fill.strategy_id]['total_value'] -= fill_cost + fill.commission

    def handle_fill_event(self, evt: FillEvent):
        # 순서 중요!!
        order_status = self.update_order_table_from_fill(evt=evt)  # update_order_table_from_fill에서 FillEvent None값 채워줌(Matcher Func)
        self.update_positions_from_fill(evt=evt)
        self.update_holdings_from_fill(evt=evt)  # holdings 의 spot usdt 부분만 업데이트!
        self.update_fill_event_to_DB(evt=evt)

        if order_status == "FILLED":
            # (Position_Redis을 업데이한 후에) OrderSuccess 이벤트 내보내기
            os_event = OrderSuccessEvent(source=evt.source,
                                         asset_type=evt.asset_type,
                                         symbol=evt.symbol,
                                         direction=evt.direction,
                                         order_uid=evt.order_uid)
            self.execution_queue.put(os_event)
            self.strategy_queue.put(os_event)

    # Order Event Update
    def handle_order_event(self, evt: OrderEvent or PairOrderEvent):
        # TODO:: 시스템 종료시 미체결 order들 다시 불러와서 Order_Pickle 만들어주는 함수 필요

        if evt.type == 'ORDER':
            strategy_id = evt.strategy_id

            # 1. Order_Table에 신규 Order 업데이트
            self.order_table[strategy_id][evt.order_uid] = evt

        if evt.type == 'PAIR_ORDER':
            strategy_id = evt.first_order.strategy_id
            first_order = evt.first_order
            second_order = evt.second_order

            # 1. Order_Table에 신규 Order 업데이트
            self.order_table[strategy_id][first_order.order_uid] = first_order
            self.order_table[strategy_id][second_order.order_uid] = second_order

    # 현재 포지션이 잔고와 일치하는지 Jango Event(n초 마다 수신) 때마다 확인
    def _check_position_status(self, api_current_holdings, api_current_positions):
        flatten_cur_pos = flatten(self.current_positions, reducer='underscore')
        flatten_api_pos = flatten(api_current_positions, reducer='underscore')

        # position이 Api와 일치하는지 체크
        for k, v in flatten_api_pos.items():
            try:
                if v == flatten_cur_pos[k]:
                    pass
                else:
                    self.logger.error(
                        f'[!!POSITION MISMATCH!!]\n"API" {k} : {v}\n"Cur_pos" {k} : {flatten_cur_pos[k]}\n@Portfolio')
            except KeyError:
                self.logger.exception(f"Cur_Pos has missing positions!! : {k} @Portfolio")

        self.logger.info(f'Position Check Success! @Port')


if __name__ == "__main__":
    cls = Portfolio()
    cls.initialize_order_table()
