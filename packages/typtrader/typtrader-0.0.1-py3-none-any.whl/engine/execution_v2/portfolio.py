import time
import json
import redis
from copy import deepcopy
from decimal import Decimal
from functools import partial
from typing import Dict, List
from flatten_dict import flatten
from multiprocessing import Queue
from collections import OrderedDict

from engine.events import (
    JangoEvent,
    SignalEvent,
    PairSignalEvent,
    OrderEvent,
    PairOrderEvent,
    FillEvent,
    OrderSuccessEvent,
)
from engine.utils.persist_db import PersistDB
from engine.utils.log import Logger, CoinTelegram
from engine.utils.distributed_queue import DistributedQueue
from params import (
    EXCHANGE_LIST,
    EXECUTION_QUEUE_HOST,
    EXECUTION_QUEUE_PORT,
    STRATEGY_QUEUE_HOST,
    EXAMPLE_STRATEGY_QUEUE_PORT,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PASSWORD,
)

STRATEGY_LS = ['example']

STRATEGY_PORTS = {
    'example': EXAMPLE_STRATEGY_QUEUE_PORT,
}


class Portfolio:

    def __init__(self,
                 execution_host: str = EXECUTION_QUEUE_HOST,
                 execution_port: int = EXECUTION_QUEUE_PORT,
                 execution_queue: Queue = None,
                 strategy_host: str = STRATEGY_QUEUE_HOST,
                 strategy_ports: Dict[str, int] = STRATEGY_PORTS,
                 strategy_queues: Dict[str, Queue] = None,
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

        self.persist_db = PersistDB()
        self.logger = Logger(debug=debug)
        self.telegram = CoinTelegram(debug=debug)

        self.jango_updated = False
        self.init_jango_sig = False

        self.strategy_ls: List[str] = strategy_ls
        self.order_table: Dict[str, OrderedDict] = self.persist_db.get('order_table',
                                                                       default={st: OrderedDict() for st in self.strategy_ls})

        # Positions만 있으면 Holdings를 구할수 있게 구현해야한다.
        self.current_positions = {}  # Account 에서 둘다 만들어서 jango event로 넘어온다.
        self.current_holdings = {}

        if not self.backtest:
            self.redis_conn = redis.StrictRedis(host=redis_host,
                                                port=redis_port,
                                                password=redis_password)

        self.spot_USDT_holdings = {}

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
                self.jango_updated = True

        elif event.type == 'JANGO' and self.init_jango_sig:
            pass

        else:
            self.logger.error('[Portfolio] Wrong JANGO request')

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

    # Redis handlers
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
            if p_q_lev in ['l', 'lev']:
                p_q_lev = 'leverage'
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
            if p_q_lev in ['l', 'lev']:
                p_q_lev = 'leverage'
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
    def update_signal_event_to_DB(self, event: SignalEvent):
        if self.backtest:
            return

        s = time.time()
        event.save()
        self.logger.debug(f'[Portfolio] Updating SignalEvent to DB took: {round(time.time() - s, 3)} sec.')

    def update_pairsignal_event_to_DB(self, event: PairSignalEvent):
        if self.backtest:
            return

        s = time.time()
        event.save()
        self.logger.debug(f'[Portfolio] Updating PairSignalEvent to DB took: {round(time.time() - s, 3)} sec.')

    def update_fill_event_to_DB(self, event: FillEvent):
        if self.backtest:
            return

        s = time.time()
        event.save()
        self.logger.debug(f'[Portfolio] Updating FillEvent to DB took: {round(time.time() - s, 3)} sec.')

    def save_order_table(self):
        if not self.backtest:
            # 로컬 persist_db 폴더에 피클 파일 저장하기
            self.persist_db.set('order_table', self.order_table)

        if not self.backtest and not self.debug:
            # 외부에서 order table을 사용할 수 있도록 Redis로 저장
            for st, table in self.order_table.items():
                ord_tab_json = {uid: evt.__dict__ for uid, evt in table.items()}
                self.redis_conn.set(f'{st}_ORDER_TABLE', json.dumps(ord_tab_json))

    def handle_order_event(self, event: OrderEvent or PairOrderEvent):
        # Order_Table에 신규 Order 업데이트
        if event.type == 'ORDER':
            strategy_id = event.strategy_id

            self.order_table[strategy_id][event.order_uid] = event
            self.save_order_table()

        if event.type == 'PAIR_ORDER':
            strategy_id = event.first_order.strategy_id
            first_order = event.first_order
            second_order = event.second_order

            self.order_table[strategy_id][first_order.order_uid] = first_order
            self.order_table[strategy_id][second_order.order_uid] = second_order
            self.save_order_table()

    def handle_fill_event(self, event: FillEvent):
        self.update_positions_from_fill(event)
        self.update_holdings_from_fill(event)
        self.update_fill_event_to_DB(event)

    # Fill Event Update
    def update_positions_from_fill(self, event: FillEvent):
        strategy_id = event.strategy_id
        exchange = event.exchange
        asset_type = event.asset_type
        symbol = event.symbol
        side = event.side
        filled_quantity = event.filled_quantity
        fill_cost = event.fill_cost
        est_fill_cost = event.est_fill_cost
        commission = event.commission
        direction = event.direction

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
        except KeyError:  # 기존 position이 없는 불특정 종목이 들어올수는 없긴함.
            self.logger.exception('[Portfolio] 기존 current_positions에 없는 불특정 종목이 들어옴')
            pos_q, pos_p = None, None

        if pos_q < 0:
            self.logger.error('[Portfolio] Position Quantity should not be Negative')

        # 1. Update Quantity
        if direction == 'ENTRY':
            updated_pos_q = float(Decimal(str(pos_q)) + Decimal(str(filled_quantity)))  # pos_q 도 abs 해줘야하는거 아닐까?
            l_s = 'long' if side == 'BUY' else 'short' if side == 'SELL' else None

            if asset_type == 'margin' and side == 'BUY':
                updated_pos_q = float(Decimal(str(pos_q)) + Decimal(str(filled_quantity)) - Decimal(str(commission)))

        elif direction == 'EXIT':
            updated_pos_q = float(Decimal(str(pos_q)) - Decimal(str(filled_quantity)))
            l_s = 'short' if side == 'BUY' else 'long' if side == 'SELL' else None

        else:
            updated_pos_q = None
            l_s = None
            self.logger.error(f'[Portfolio] Direction should be ENTRY or EXIT : {direction}')

        set_redis = partial(self.redis_position_setter,
                            strategy_id=strategy_id,
                            exchange=exchange,
                            asset_type=asset_type,
                            symbol=symbol)

        self.current_positions[strategy_id][exchange][asset_type][symbol][l_s]['q'] = updated_pos_q
        set_redis(long_short=l_s, p_q_lev='q', value=updated_pos_q)

        # 2. Update Average Price

        # 전량 Exit 된 경우
        if updated_pos_q == 0:
            if side == 'BUY':
                for p_q_lev in ['p', 'q', 'leverage']:
                    self.current_positions[strategy_id][exchange][asset_type][symbol]['long'][p_q_lev] = 0
                    set_redis(long_short='long', p_q_lev=p_q_lev, value=0)
            elif side == 'SELL':
                for p_q_lev in ['p', 'q', 'leverage']:
                    self.current_positions[strategy_id][exchange][asset_type][symbol]['short'][p_q_lev] = 0
                    set_redis(long_short='short', p_q_lev=p_q_lev, value=0)
        else:
            if direction == 'ENTRY':
                if side == 'BUY':
                    value = ((pos_q * pos_p) + fill_cost) / updated_pos_q
                    self.current_positions[strategy_id][exchange][asset_type][symbol]['long']['p'] = value
                    set_redis(long_short='long', p_q_lev='p', value=value)
                elif side == 'SELL':
                    value = ((pos_q * pos_p) + fill_cost) / updated_pos_q
                    self.current_positions[strategy_id][exchange][asset_type][symbol]['short']['p'] = value
                    set_redis(long_short='short', p_q_lev='p', value=value)
            elif direction == 'EXIT':
                if side == 'BUY':
                    self.current_positions[strategy_id][exchange][asset_type][symbol]['short']['p'] = pos_p
                    set_redis(long_short='short', p_q_lev='p', value=pos_p)
                elif side == 'SELL':
                    self.current_positions[strategy_id][exchange][asset_type][symbol]['long']['p'] = pos_p
                    set_redis(long_short='long', p_q_lev='p', value=pos_p)

        self.logger.info(f'[Portfolio] 체결 업데이트 완료: {self.current_positions[strategy_id][exchange][asset_type][symbol]}')

    def update_holdings_from_fill(self, event: FillEvent):
        """
        Holdings 정보는 spot USDT 수량만 event driven 방식으로 Redis로 업데이트해주고,
        주기적으로 Holdings Tracker에서 나머지를 업데이트해준다. (현재 연산 속도가 오래 걸려서 취한 임시방편)
        """
        strategy_id = event.strategy_id
        exchange = event.exchange
        asset_type = event.asset_type
        symbol = event.symbol
        side = event.side
        filled_quantity = event.filled_quantity
        fill_cost = event.fill_cost
        est_fill_cost = event.est_fill_cost
        commission = event.commission
        direction = event.direction

        fill_dir = -1 if direction == 'ENTRY' else 1 if direction == 'EXIT' else None

        if direction == 'ENTRY':
            l_s = 'long' if side == 'BUY' else 'short'
        elif direction == 'EXIT':
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

        self.spot_USDT_holdings[exchange] += (fill_dir / lev) * fill_cost

        self.redis_holdings_setter(strategy_id=strategy_id,
                                   exchange=exchange,
                                   asset_type='spot',
                                   symbol='USDT',
                                   value=self.spot_USDT_holdings[exchange])


if __name__ == '__main__':
    sig_evt = SignalEvent(strategy_id='example',
                          exchange='binance',
                          asset_type='usdt',
                          symbol='ETHUSDT',
                          signal_type='ENTRY',
                          signal_price=0.3,
                          order_type='MKT')

    ord_evt = OrderEvent(strategy_id='example',
                         exchange='binance',
                         asset_type='usdt',
                         symbol='ETHUSDT',
                         order_type='MKT',
                         quantity=50,
                         price=None,
                         side='BUY',
                         direction='ENTRY',
                         leverage_size=1,
                         invest_amount=0.3 * 50,
                         margin_type='ISOLATED',
                         est_fill_cost=0,
                         signal_uid=sig_evt.signal_uid,
                         paired=False)


    # execution_queue = DistributedQueue(EXECUTION_QUEUE_PORT)
    #
    # event = execution_queue.get()

    port = Portfolio(debug=True)
    # port.update_jango(event, method='self_update')

    port.handle_order_event(ord_evt)