import time
import traceback
from typing import Dict, List
from multiprocessing import Queue
from cointraderkr import BybitAPI, BinanceAPI

from engine.utils.log import Logger
from engine.events import JangoEvent
from engine.utils.distributed_queue import DistributedQueue
from params import (
    API_KEYS,
    EXCHANGE_LIST,
    ASSET_LIST,
    SYMBOL_LIST,
    EXECUTION_QUEUE_HOST,
    EXECUTION_QUEUE_PORT,
)

STRATEGY_LS = ['example']


class AccountHandler:

    API_RETRY_TIME = 5

    def __init__(self,
                 jango_req_time: int = 60 * 10,  # 10분에 한번씩 실행
                 execution_host: str = EXECUTION_QUEUE_HOST,
                 execution_port: int = EXECUTION_QUEUE_PORT,
                 execution_queue: Queue = None,
                 strategy_ls: List[str] = STRATEGY_LS,
                 start_money: int or float = 0.0,
                 debug: bool = False):

        self.debug = debug
        self.JANGO_REQ_TIME = jango_req_time

        self.start_money = start_money  # backtest 전용
        self.logger = Logger(debug=debug)

        if execution_queue is None:
            self.execution_queue = DistributedQueue(execution_port, execution_host)
            print(f'[Account] Created Execution DistributedQueue at tcp://{execution_host}:{execution_port}')
        else:
            self.execution_queue = execution_queue

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

        # account_setup에서 새팅
        self.cur_pos_structure = None
        self.cur_hold_structure = None

        self.bybit_request_error_cnt = 0

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

            if a in ['spot', 'usdt']:
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

    # Isolated Account 기준!
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

        for a in bi_usdt['assets']:
            symbol = a['asset']
            if symbol == 'USDT':
                self.cur_hold_structure[st]['binance']['usdt'][symbol] = float(a['walletBalance'])

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
        """
        Bybit는 전략을 돌리기 전에 미리 USDT 마켓으로 돈을 옮겨둬야 한다.
        아래에 spot USDT는 실상 usdt 계좌 USDT 수량이라고 보면 된다.
        """
        try:
            bi_usdt = self.bybit_api[st].get_usdt_futures_positions(symbol=None)
            usdt_balance = self.bybit_api[st].get_balance()
            self.cur_hold_structure[st]['bybit']['spot']['USDT'] = float(usdt_balance['USDT']['wallet_balance'])

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

            # TODO: add coinm later
            # self.binance_coinm_account_setup(st)

            self.bybit_usdt_account_setup(st)

    def backtest_account_setting(self):
        self.cur_pos_structure = {st: self.init_current_positions() for st in self.strategy_ls}
        self.cur_hold_structure = {st: self.init_current_holdings() for st in self.strategy_ls}

        for st in self.strategy_ls:
            for e in EXCHANGE_LIST:
                self.cur_hold_structure[st][e]['spot']['USDT'] = self.start_money

        jango_event = JangoEvent(self.cur_hold_structure, self.cur_pos_structure)
        self.execution_queue.put(jango_event)

    def start_account_loop(self):
        while True:
            try:
                s = time.time()

                self.account_setup()
                jango_event = JangoEvent(self.cur_hold_structure, self.cur_pos_structure)
                self.execution_queue.put(jango_event)

                e = time.time()
                self.logger.info(f'[Account] Jango setup took: {e - s}')
                time.sleep(self.JANGO_REQ_TIME)
            except:
                traceback.print_exc()
                self.logger.info(f'[Account] start_account_loop: Retrying request to API....wait for 5 sec and retry')
                time.sleep(self.API_RETRY_TIME)


if __name__ == '__main__':
    acc = AccountHandler()
    # acc.account_setup()
    print(acc)
    acc.start_account_loop()
