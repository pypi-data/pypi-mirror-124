import time
import json
import traceback
from decimal import Decimal
from typing import Dict, List
from multiprocessing import Queue
from cointraderkr import BybitAPI, BinanceAPI

from params import (
    EXCHANGE_LIST,
    ASSET_LIST,
    SYMBOL_LIST,
    API_KEYS,
)
from engine.utils.log import Logger
from api.data_client import DataClient
from engine.utils.distributed_queue import DistributedQueue
from engine.events import (
    JangoEvent,
    TransferSuccessEvent,
    RepaySuccessEvent,
    LeverageSuccessEvent,
    MarginTypeSuccessEvent,
    FillEvent,
)
from params import (
    PROXY_HOST,
    DATA_PROXY_ACCOUNT_PORT,
    ACCOUNT_QUEUE_HOST,
    ACCOUNT_QUEUE_PORT,
    EXECUTION_QUEUE_HOST,
    EXECUTION_QUEUE_PORT,
    LOG_QUEUE_HOST,
    LOG_QUEUE_PORT,
)

STRATEGY_LS = ['example']


class AccountHandler:

    def __init__(self,
                 account_proxy_host: str = PROXY_HOST,
                 account_proxy_port: int = DATA_PROXY_ACCOUNT_PORT,
                 account_host: str = ACCOUNT_QUEUE_HOST,
                 account_port: int = ACCOUNT_QUEUE_PORT,
                 account_queue: Queue = None,
                 execution_host: str = EXECUTION_QUEUE_HOST,
                 execution_port: int = EXECUTION_QUEUE_PORT,
                 execution_queue: Queue = None,
                 log_host: str = LOG_QUEUE_HOST,
                 log_port: int = LOG_QUEUE_PORT,
                 start_money: float = 0.0,
                 strategy_ls: List[str] = STRATEGY_LS,
                 debug: bool = False):
        """
        :param account_proxy_host: DataClient가 사용하는 스트림 서버 호스트
        :param account_proxy_port: DataClient가 사용하는 스트림 서버 포트
        :param account_host:
        :param account_port:
        :param account_queue:
        :param execution_host:
        :param execution_port:
        :param execution_queue:
        :param log_host:
        :param log_port:
        :param start_money:
        :param strategy_ls:
        :param debug:
        """

        print(f'[Account] Starting with: {strategy_ls}')

        self.debug = debug

        self.account_proxy_host = account_proxy_host
        self.account_proxy_port = account_proxy_port

        if account_queue is None:
            self.account_queue = DistributedQueue(account_port, account_host)
            print(f'[Account] Created Account DistributedQueue at tcp://{account_host}:{account_port}')
        else:
            self.account_queue = account_queue

        if execution_queue is None:
            self.execution_queue = DistributedQueue(execution_port, execution_host)
            print(f'[Account] Created Execution DistributedQueue at tcp://{execution_host}:{execution_port}')
        else:
            self.execution_queue = execution_queue

        self.logger = Logger(log_port, log_host, debug=debug)

        self.start_money = start_money # backtest 전용
        self.strategy_ls = strategy_ls

        self.binance_api: Dict[str, BinanceAPI] = {
            st: BinanceAPI(public_key=API_KEYS[st]['binance_public'],
                           secret_key=API_KEYS[st]['binance_private'])
            for st in strategy_ls
        }
        self.bybit_api: Dict[str, BybitAPI] = {
            st: BybitAPI(public_key=API_KEYS[st]['bybit_public'],
                         private_key=API_KEYS[st]['bybit_private'])
            for st in strategy_ls
        }

        self.cur_pos_structure = None
        self.cur_hold_structure = None

        self.bybit_request_error_cnt = 0

    def get_positions(self, strategy: str, exchange: str, asset: str, symbol: str):
        return self.cur_pos_structure.get(strategy, {})\
                                     .get(exchange, {})\
                                     .get(asset, {})\
                                     .get(symbol)

    def get_holdings(self, strategy: str, exchange: str, asset: str, symbol: str):
        return self.cur_hold_structure.get(strategy, {})\
                                      .get(exchange, {})\
                                      .get(asset, {})\
                                      .get(symbol)

    # Current_Pos & Current_Holdings Initialize
    def _bi_init_current_positions(self):
        bi_pos_dict = {}
        for a in ASSET_LIST:
            bi_pos_dict[a] = {}
            for s in SYMBOL_LIST:
                if a == 'coinm':
                    s = s.replace('USDT', 'USD')
                bi_pos_dict[a][s] = {'long': {'q': 0.0, 'p': 0.0, 'leverage': 0.0},
                                     'short': {'q': 0.0, 'p': 0.0, 'leverage': 0.0}}
        return bi_pos_dict

    def _by_init_current_positions(self):
        # Bybit는 usdt 마켓만 사용한다. (spot/coinm은 추후 추가 예정)
        by_pos_dict = {'usdt': {}}
        for s in SYMBOL_LIST:
            by_pos_dict['usdt'][s] = {'long': {'q': 0.0, 'p': 0.0, 'leverage': 0.0},
                                      'short': {'q': 0.0, 'p': 0.0, 'leverage': 0.0}}
        return by_pos_dict

    def init_current_positions(self):
        bi_pos_dict = self._bi_init_current_positions()
        by_pos_dict = self._by_init_current_positions()
        cur_pos_dict = {'binance': bi_pos_dict, 'bybit': by_pos_dict}
        return cur_pos_dict

    def _bi_init_current_holdings(self):
        bi_cur_hold_dict = {}
        for a in ASSET_LIST:
            bi_cur_hold_dict[a] = {}
            if a != 'coinm':
                bi_cur_hold_dict[a]['TotalValue'] = 0.0

            if a == 'spot':
                bi_cur_hold_dict[a]['USDT'] = 0.0  # Isolated는 spot 만 USDT있으면됨
            # bi_cur_hold_dict[a]['commission'] = 0.0

            for s in SYMBOL_LIST:
                bi_cur_hold_dict[a][s] = 0.0
            # else:
            #     bi_cur_hold_dict['coinm']['BTCUSD'] = 0.0
            #     bi_cur_hold_dict['coinm']['BTCUSD_leftovers'] = 0.0
        return bi_cur_hold_dict

    def _by_init_current_holdings(self):
        by_cur_hold_dict = {'spot': {}, 'usdt': {}}

        by_cur_hold_dict['spot']['USDT'] = 0.0
        by_cur_hold_dict['usdt']['TotalValue'] = 0.0
        # by_cur_hold_dict['usdt']['commission'] = 0.0

        for s in SYMBOL_LIST:
            by_cur_hold_dict['usdt'][s] = 0.0
        return by_cur_hold_dict

    def init_current_holdings(self):
        by_cur_hold_dict = self._by_init_current_holdings()
        bi_cur_hold_dict = self._bi_init_current_holdings()
        cur_hold_dict = {'binance': bi_cur_hold_dict, 'bybit': by_cur_hold_dict}
        return cur_hold_dict

    ########## [Request Jango Start] ############
    def binance_spot_account_setup(self, st: str):
        # Spot Account는 q 와 lev가 불필요 하다.
        bi_spot = self.binance_api[st].get_account('MAIN')
        spot_SYMBOL_LIST = [s.replace('USDT', '') for s in SYMBOL_LIST]
        if bi_spot['accountType'] == 'SPOT':  # spot에 대한 accountType이 Margin으로 돼있음 --> 다시 SPOT 으로 바뀜;;
            for a in bi_spot['balances']:
                if a['asset'] == 'USDT':  # 현금
                    self.cur_hold_structure[st]['binance']['spot']['USDT'] = float(a['free'])
                if a['asset'] in spot_SYMBOL_LIST:
                    # TODO: 추후 지정가 주문을 고려하기 시작하면 locked 변수도 트래킹이 되어야 한다. 시장가에서는 제외.
                    self.cur_pos_structure[st]['binance']['spot'][f"{a['asset']}USDT"]['long']['q'] = abs(float(a['free']))
        else:
            # 아래와 같은 오류는 binance_api가 잘못되었을 경우 발생하는 오류 (trader api만 괜찮다면 발생할 일 없음)
            log_msg = f'[Account] binance_spot_account_setup: accountType is not SPOT: {bi_spot["accountType"]}'
            self.logger.error(log_msg)

    # Isolated Account 기준!!
    def binance_margin_account_setup(self, st: str):
        # 추후 margin short long 원리 정리 되면 코드 재정비 필요
        bi_margin = self.binance_api[st].get_isolated_margin_account()
        margin_SYMBOL_LIST = [s.replace('USDT', '') for s in SYMBOL_LIST]
        for u in bi_margin['assets']:
            if u['baseAsset']['asset'] in margin_SYMBOL_LIST:
                TA = float(u['baseAsset']['netAssetOfBtc'])
                TE = float(u['baseAsset']['netAssetOfBtc']) + float(u['quoteAsset']['netAssetOfBtc'])

                q = abs(float(u['baseAsset']['netAsset']))

                # 짤짤이 관리...필요할까? Reset만 잘한다면 짤짤이는 지갑에 안넣어줘도 될듯하다. 만약 Reset없이 지갑을 이어가고 싶으면 무조건 필요.

                # LONG 진입 SHORT 청산인 경우에는 usdt를 빌리고 청산을 하기 때문에 borrowed 했던 코인에 영향을 받지 않는다. borrowed를 추가하면 long 청산시 error 발생
                symbol = u['symbol']
                self.cur_pos_structure[st]['binance']['margin'][symbol]['long']['q'] = float(
                    u['baseAsset']['totalAsset'])
                # SHORT 진입 LONG 청산인 경우에는 코인을 빌린걸 되팖으로 borrowed를 기준으로 봐야한다.
                self.cur_pos_structure[st]['binance']['margin'][symbol]['short']['q'] = float(
                    u['baseAsset']['borrowed'])

                try:
                    lev = abs(TA) / TE
                    if lev < 1:
                        lev = 0
                except ZeroDivisionError:
                    lev = 0

                for l_s in ['long', 'short']:
                    self.cur_pos_structure[st]['binance']['margin'][u['symbol']][l_s]['leverage'] = lev

    # Isolated 기준으로 설계된거 맞나 확인하기!
    def binance_usdt_account_setup(self, st: str):
        bi_usdt = self.binance_api[st].get_account('UMFUTURE')
        usdt_SYMBOL_LIST = SYMBOL_LIST

        for p in bi_usdt['positions']:
            symbol = p['symbol']
            if symbol in usdt_SYMBOL_LIST:
                q = float(p['positionAmt'])
                # LONG
                if q >= 0:
                    self.cur_pos_structure[st]['binance']['usdt'][symbol]['long']['p'] = float(p['entryPrice'])
                    self.cur_pos_structure[st]['binance']['usdt'][symbol]['long']['q'] = q
                    self.cur_pos_structure[st]['binance']['usdt'][symbol]['long']['leverage'] = float(p['leverage'])
                # SHORT
                else:
                    self.cur_pos_structure[st]['binance']['usdt'][symbol]['short']['p'] = float(p['entryPrice'])
                    self.cur_pos_structure[st]['binance']['usdt'][symbol]['short']['q'] = abs(q)
                    self.cur_pos_structure[st]['binance']['usdt'][symbol]['short']['leverage'] = float(p['leverage'])

                self.cur_hold_structure[st]['binance']['usdt'][symbol] = float(p['positionInitialMargin']) + \
                                                                         float(p['unrealizedProfit'])

    def binance_coinm_account_setup(self, st: str):
        """
        coin-m 에서는 현재는 펀딩피 전략만 진행.
        따라서 전략을 진행하는데 필요한 전체 Position Quantity와 펀딩피(+소량의 초기투자 잔여금)의 누적분인 Leftover를 구하여
        추후 leftover가 1 contract($100) 이상의 가치를 가지면 재투자 진행.
        Isolated로 투자하고 있음으로 펀딩피가 IsolatedWallet에 쌓인다. (Initial Margin과의 차이분이 Leftover!)
        """
        # TODO :: 펀딩피 전략 실행할 코인 종류 더 추가하기.
        bi_coinm = self.binance_api[st].get_account('CMFUTURE')
        for a in bi_coinm['assets']:
            if a['asset'] == 'BTC':
                self.cur_pos_structure[st]['binance']['coinm']['BTCUSD']['total_balance'] = float(
                    a['marginBalance'])  # 'marginBalance' = 'walletBalance'(펀딩피 포함됨) + 'unrealizedProfit' 이것만 트레킹 하면됨.
                # self.cur_pos_structure['binance']['coinm']['BTC']['availableBalance'] = a['availableBalance'] # 남은 짤짤이
        for p in bi_coinm['positions']:
            if p['symbol'] == 'BTCUSD_PERP':
                # isolated 계좌에 펀딩피가 쌓임. Leftover의 가치가 $100 이상이 되면 1 contract 추가계약 하면된다.
                self.cur_pos_structure[st]['binance']['coinm']['BTCUSD']['leftovers'] = float(
                    p['isolatedWallet']) - float(p['initialMargin'])

    def bybit_usdt_account_setup(self, st: str):
        try:
            bi_usdt = self.bybit_api[st].get_usdt_futures_positions(symbol=None)
            self.cur_hold_structure[st]['bybit']['spot']['USDT'] = float(
                self.bybit_api[st].get_balance()['USDT']['wallet_balance'])

            for i in range(len(bi_usdt)):
                usdt_SYMBOL_LIST = bi_usdt[i]['data']['symbol']

                if (bi_usdt[i]['data']['side'] == 'Buy') & (float(bi_usdt[i]['data']['size']) > 0):
                    self.cur_pos_structure[st]['bybit']['usdt'][usdt_SYMBOL_LIST]['long']['p'] = float(
                        bi_usdt[i]['data']['entry_price'])
                    self.cur_pos_structure[st]['bybit']['usdt'][usdt_SYMBOL_LIST]['long']['q'] = abs(float(
                        bi_usdt[i]['data']['size']))
                    self.cur_pos_structure[st]['bybit']['usdt'][usdt_SYMBOL_LIST]['long']['leverage'] = float(
                        bi_usdt[i]['data']['leverage'])

                elif (bi_usdt[i]['data']['side'] == 'Sell') & (float(bi_usdt[i]['data']['size']) > 0):
                    self.cur_pos_structure[st]['bybit']['usdt'][usdt_SYMBOL_LIST]['short']['p'] = float(
                        bi_usdt[i]['data']['entry_price'])
                    self.cur_pos_structure[st]['bybit']['usdt'][usdt_SYMBOL_LIST]['short']['q'] = abs(float(
                        bi_usdt[i]['data']['size']))
                    self.cur_pos_structure[st]['bybit']['usdt'][usdt_SYMBOL_LIST]['short']['leverage'] = float(
                        bi_usdt[i]['data']['leverage'])
        except TypeError:
            self.bybit_request_error_cnt += 1

            traceback.print_exc()
            log_msg = f'[Account] bybit_usdt_account_cleanse: Bybit account request error. Error count: {self.bybit_request_error_cnt}'
            self.logger.exception(log_msg)

    def account_setup(self):
        """
        {
            'strategy_name': {
                'exchange_name': {
                    'asset_type': {
                        'symbol': ...
                    },
                },
            },
        }
        """
        self.cur_pos_structure = {st: self.init_current_positions() for st in self.strategy_ls}
        self.cur_hold_structure = {st: self.init_current_holdings() for st in self.strategy_ls}

        for st in self.strategy_ls:
            self.binance_spot_account_setup(st)
            self.binance_margin_account_setup(st)
            self.binance_usdt_account_setup(st)

            # TODO: coinm 추가하기
            # self.binance_coinm_account_setup(st)

            self.bybit_usdt_account_setup(st)
    ########## [Request Jango End] ############

    def order_check(self, data: dict):
        """
        OrderSuccess를 보내지 않는 이유 상의
        """
        pass

    def fill_check(self, data: dict):
        if data['source'] == 'binance':
            if data['type'] == 'usdt_futures_account':
                if data['e'] == 'ORDER_TRADE_UPDATE':
                    symbol = data['o']['s']
                    side = data['o']['S']
                    order_quantity = float(data['o']['q'])  # 주문수량
                    fill_quantity = float(data['o']['l'])  # 체결수량
                    cum_fill_quantity = float(
                        data['o']['z'])  # 누적 체결수량 앞서 체결된 partially_filled 까지 다 포함해서 해당 오더에 대한 전체 체결 수량
                    order_price = float(data['o']['ap'])  # 주문가격
                    fill_price = float(data['o']['L'])  # 체결가격
                    api_order_uid = data['o']['c']

                    try:
                        commission = float(data['o']['n'])  # 수수료
                    except KeyError:
                        commission = None

                    fill_event = FillEvent(exchange='binance',
                                           asset_type='usdt',
                                           symbol=symbol,
                                           filled_quantity=fill_quantity,
                                           order_quantity=order_quantity,
                                           side=side,
                                           fill_cost=fill_quantity * fill_price,
                                           est_fill_cost=order_quantity * order_price,
                                           api_order_uid=api_order_uid,
                                           commission=commission)

                    if data['o']['X'] == 'FILLED':  # 주문 체결
                        self.logger.info(f"#### [BINANCE USDT] FILLED ORDER #### : {fill_event.__dict__}")
                        self.execution_queue.put(fill_event)

                    elif data['o']['X'] == 'PARTIALLY_FILLED':
                        self.logger.info(f"#### [BINANCE USDT] PARTIALLY_FILLED ORDER #### : {fill_event.__dict__}")
                        self.execution_queue.put(fill_event)

                    elif data['o']['x'] == 'NEW':  # 주문 접수
                        pass
                        # self.logger.info(f"#### [USDT] NEW FILL ORDER ####"
                        #                  f"\nExchange: Binance"
                        #                  f"\nAssetType: USDT"
                        #                  f"\nTime: {datetime.datetime.now()}"
                        #                  f"\nSymbol: {symbol}"
                        #                  f"\nQuantity: {order_quantity}"
                        #                  f"\nSide: {side}")
                        # print("NEW ###", data)

                    else:
                        self.logger.debug(f"[참고] passing binance usdt order trade updates: {data} @ Account")

            if data['type'] == 'isolated_margin_account':
                if data['event_type'] == 'executionReport':
                    symbol = data['symbol']
                    side = data['side']
                    order_quantity = float(data['order_quantity'])         # 주문수량
                    fill_quantity = float(data['last_executed_quantity'])  # 체결수량
                    order_price = None                                     # 주문가격, margin인 경우 q로 주문넣으면 order_price 0으로 찍힘..
                    fill_price = float(data['last_executed_price'])        # 체결가격
                    commission = float(data['commission_amount'])          # 수수료
                    api_order_uid = data['client_order_id']

                    fill_event = FillEvent(exchange='binance',
                                           asset_type='margin',
                                           symbol=symbol,
                                           filled_quantity=fill_quantity,
                                           order_quantity=order_quantity,
                                           side=side,
                                           fill_cost=fill_quantity * fill_price,
                                           est_fill_cost=None if order_price is None else order_quantity * order_price,
                                           api_order_uid=api_order_uid,
                                           commission=commission)

                    if data['current_order_status'] == 'FILLED':
                        self.logger.info(f"#### [BINANCE MARGIN] FILLED ORDER #### : {fill_event.__dict__}")
                        self.execution_queue.put(fill_event)

                    elif data['current_order_status'] == 'PARTIALLY_FILLED':
                        self.logger.info(f"#### [BINANCE MARGIN] PARTIALLY_FILLED ORDER #### : {fill_event.__dict__}")
                        self.execution_queue.put(fill_event)

                    elif data['current_order_status'] == 'NEW':
                        pass
                        # self.logger.info(f"#### [MARGIN] NEW FILL ORDER ####"
                        #                  f"\nExchange: Binance"
                        #                  f"\nAssetType: MARGIN"
                        #                  f"\nTime: {datetime.datetime.now()}"
                        #                  f"\nSymbol: {symbol}"
                        #                  f"\nQuantity: {order_quantity}"
                        #                  f"\nSide: {side}")
                    else:
                        self.logger.debug(f"[참고] passing binance margin execution report: {data}")
                else:
                    self.logger.debug(f"[참고] passing binance margin data: {data}")

        # TODO :: Bybit fill_event는 미완성이다. data['type']의 order과 execution의 차이 구분 필요.
        # 현재로는 execution이 개별체결내역을 보여주는듯해 채택함
        # 또한 Bybit는 New Order 개념이 시장가 주문에서는 확인 불가함.

        if data['source'] == 'bybit':
            if data['asset_type'] == 'usdt':
                if data['type'] == 'execution':
                    fill_quantity = 0
                    commission = 0
                    weighted_fill_price = 0

                    strategy_id = data['name']
                    symbol = None
                    side = None
                    order_quantity = None
                    avg_fill_price = None
                    order_price = None
                    api_order_uid = None

                    for i in range(len(data['data'])):
                        symbol = data['data'][i]['symbol']
                        side = data['data'][i]['side'].upper()
                        order_quantity = float(data['data'][i]['order_qty'])  # 주문수량
                        exec_quantity = Decimal(str(data['data'][i]['exec_qty']))
                        fill_quantity += exec_quantity  # 체결수량 (A)
                        order_price = None  # 주문가격, 현재 fill_price로 쓰는 price가 order_price 일수도 있음 추후 확인필요.
                        weighted_fill_price += float(data['data'][i]['price']) * float(exec_quantity)  # 체결가격 가중 합 (B)
                        avg_fill_price = weighted_fill_price / float(fill_quantity)  # 체결가격 가중평균 (B/A)
                        commission += float(data['data'][i]['exec_fee'])  # 수수료
                        api_order_uid = data['data'][i]['order_id']

                    if symbol is not None:
                        fill_event = FillEvent(strategy_id=strategy_id,
                                               exchange='bybit',
                                               asset_type='usdt',
                                               symbol=symbol,
                                               filled_quantity=float(fill_quantity),
                                               order_quantity=order_quantity,
                                               side=side,
                                               fill_cost=float(fill_quantity) * avg_fill_price,
                                               est_fill_cost=None if order_price is None else order_quantity * order_price,
                                               api_order_uid=api_order_uid,
                                               commission=commission)
                        self.execution_queue.put(fill_event)
                else:
                    self.logger.error(f"missing bybit usdt acc msg: {data} @ Account")

                    ## Bybit는 New Order 개념이 시장가 주문에서는 확인 불가함.

    def margin_type_leverage_check(self, data: dict):
        if data['source'] == 'binance':
            if data['type'] == 'usdt_futures_account':
                if data['e'] == 'ACCOUNT_CONFIG_UPDATE':
                    leverage_event = LeverageSuccessEvent(source='binance',
                                                          asset_type='usdt',
                                                          symbol=data['ac']['s'],
                                                          leverage=data['ac']['l'])
                    self.execution_queue.put(leverage_event)
                elif data['e'] == 'ACCOUNT_UPDATE':
                    if data['a']['m'] == 'MARGIN_TYPE_CHANGE':
                        margin_event = MarginTypeSuccessEvent(source='binance',
                                                              asset_type='usdt',
                                                              symbol=data['a']['P'][0]['s'],
                                                              margin_type='ISOLATED' if data['a']['P'][0][
                                                                                            'mt'] == 'isolated' else 'CROSSED')
                        self.execution_queue.put(margin_event)

        if data['source'] == 'bybit':
            if data['type'] == 'position':
                if len(data['data']) == 2:  # length가 1개인 position msg 도 돌아옴, 주문체결될때.
                    if data['data'][0]['size'] == 0 and data['data'][1]['size'] == 0:  # 처음 Leverage 바꿀때는 Position 없어야한다!
                        long_lev = float(data['data'][0]['leverage'])
                        short_lev = float(data['data'][1]['leverage'])

                        if long_lev != short_lev:
                            self.logger.error(f'[Account] Bybit leverage unmatched: {long_lev} != {short_lev}')

                        strategy_id = data['name']
                        leverage_event = LeverageSuccessEvent(strategy_id=strategy_id,
                                                              exchange='bybit',
                                                              asset_type='usdt',
                                                              symbol=data['data'][0]['symbol'],
                                                              leverage=long_lev)

                        margin_event = MarginTypeSuccessEvent(strategy_id=strategy_id,
                                                              exchange='bybit',
                                                              asset_type='usdt',
                                                              symbol=data['data'][0]['symbol'],
                                                              margin_type='CROSSED' if long_lev == 100 else 'ISOLATED')
                        self.execution_queue.put(leverage_event)
                        self.execution_queue.put(margin_event)
                else:
                    # Lev Change가 아닌 주문에 따른 position msg로 인해 발생. ERROR 아님 (or Bybit 수동 입출금시)
                    pass

    def transfer_check(self, data):
        if data['source'] == 'binance':
            if data['type'] == 'usdt_futures_account':
                if data['e'] == 'ACCOUNT_UPDATE':
                    if data['a']['m'] == 'DEPOSIT' or data['a']['m'] == 'WITHDRAW':
                        transfer_event = TransferSuccessEvent(source='binance',
                                                              asset_type='usdt',
                                                              symbol=None,
                                                              # binance response에서 symbol정보를 주지 않기 때문, spot -> usdt로 옮겼기 때문에 발생하는 당연한 이슈
                                                              amount=float(data['a']['B'][0]['bc']))
                        self.execution_queue.put(transfer_event)

            elif data['type'] == 'isolated_margin_account':
                if data['event_type'] == 'balanceUpdate':
                    transfer_event = TransferSuccessEvent(source='binance',
                                                          asset_type='margin',
                                                          symbol=data['symbol'],
                                                          amount=float(data[
                                                                           'balance_delta']))  # isolated_margin인 경우는 symbol 마다 지갑잇음
                    self.logger.debug(f"transfer success?? {data}")
                    self.execution_queue.put(transfer_event)

    def repay_check(self, data):
        if data['source'] == 'binance':
            if data['type'] == 'isolated_margin_account':
                repay_event = RepaySuccessEvent(source='binance',
                                                asset_type='margin',
                                                symbol=data['symbol'],
                                                asset=data['asset'],
                                                amount=float(
                                                    data['balance_delta']))  # Amount가 Repay 할때 음수로 나옴. 양수이면 빌려오는거임
                self.execution_queue.put(repay_event)

    def account_data_callback(self, data: dict):
        if data.get('type') != 'socket_status':
            print(data)

        # TODO :: Coin Api에서 fill_event 양식에 맞게 보내줘야함 -> 받은 fill_event를 execution_queue로 전송!
        if data['source'] == 'binance':
            if data['type'] == 'usdt_futures_account':
                if data['e'] == 'ORDER_TRADE_UPDATE':
                    self.fill_check(data)
                elif data['e'] == 'ACCOUNT_CONFIG_UPDATE':
                    self.margin_type_leverage_check(data)
                elif data['e'] == 'ACCOUNT_UPDATE':
                    self.transfer_check(data)
                    self.margin_type_leverage_check(data)
            elif data['type'] == 'isolated_margin_account':
                if data['event_type'] == 'executionReport':
                    self.fill_check(data)
                elif data['event_type'] == 'balanceUpdate':
                    if data['asset'] == 'USDT':
                        self.transfer_check(data)
                    else:
                        # short 포지션을 repay하는 경우 usdt로 repay하는 경우는 없기 때문
                        self.repay_check(data)
            else:
                if data['type'] != 'socket_status':
                    self.logger.error(f"passing Account Msg from {data['source']}_{data['type']} @ Account")

        elif data['source'] == 'bybit':
            if data['asset_type'] == 'usdt':
                if data['type'] == 'order':
                    self.order_check(data)
                elif data['type'] == 'execution':
                    self.fill_check(data)
                elif data['type'] == 'position':
                    self.margin_type_leverage_check(data)  # leverage check 안에서 size가 0인걸로 걸러서 처리함

        else:
            self.logger.error(f'[Account] Unexpected Msg: {json.dumps(data)}')

    def start_account_loop(self):
        # Starting account data stream by opening a new thread (done within DataClient)
        client = DataClient(account_host=self.account_proxy_host,
                            account_port=self.account_proxy_port,
                            debug=self.debug)
        client.stream_account_data(callback=self.account_data_callback)

        while True:
            try:
                s = time.time()
                self.account_setup()

                jango_event = JangoEvent(self.cur_hold_structure, self.cur_pos_structure)
                self.execution_queue.put(jango_event)

                e = time.time()
                print(f'Jango setup took: {e - s}')
                time.sleep(600)  # 10분에 한번씩 실행
            except:
                traceback.print_exc()
                self.logger.info(f'[Account] start_account_loop: Retrying request to API....wait for 5 sec and retry')
                time.sleep(5)

    def backtest_account_setting(self):
        self.cur_pos_structure = {st: self.init_current_positions() for st in self.strategy_ls}
        self.cur_hold_structure = {st: self.init_current_holdings() for st in self.strategy_ls}

        for st in self.strategy_ls:
            for e in EXCHANGE_LIST:
                self.cur_hold_structure[st][e]['spot']['USDT'] = self.start_money

        jango_event = JangoEvent(self.cur_hold_structure, self.cur_pos_structure)
        self.execution_queue.put(jango_event)


if __name__ == "__main__":
    ah = AccountHandler(debug=True)
    ah.start_account_loop()

    print(ah)