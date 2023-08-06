import time
import traceback
import threading
from typing import Dict, List
from multiprocessing import Queue
from cointraderkr import CoinAPI, MIN_TRADE_AMOUNT

from engine.utils.log import Logger
from engine.portfolio import Portfolio
from engine.events import (
    OrderEvent,
    PairOrderEvent,
    LeverageSuccessEvent,
    MarginTypeSuccessEvent,
    FillEvent,
)
from engine.utils.distributed_queue import DistributedQueue
from params import (
    API_KEYS,
    EXECUTION_QUEUE_HOST,
    EXECUTION_QUEUE_PORT,
    STRATEGY_QUEUE_HOST,
    EXAMPLE_STRATEGY_QUEUE_PORT,
    COIN_ARBIT_STRATEGY_QUEUE_PORT,
    LOG_QUEUE_HOST,
    LOG_QUEUE_PORT,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PASSWORD,
)

STRATEGY_LS = ['example', 'coin_arbit']

STRATEGY_PORTS = {
    'example': EXAMPLE_STRATEGY_QUEUE_PORT,
    'coin_arbit': COIN_ARBIT_STRATEGY_QUEUE_PORT,
}


class ExecutionHandler:

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
                 port_cls: Portfolio = None,
                 strategy_ls: List[str] = STRATEGY_LS,
                 backtest: bool = False,
                 debug: bool = False):

        if execution_queue is None:
            self.execution_queue = DistributedQueue(execution_port, execution_host)
            print(f'[Execution] Created Execution DistributedQueue at tcp://{execution_host}:{execution_port}')
        else:
            self.execution_queue = execution_queue

        if strategy_queues is None:
            self.strategy_queues = {st: DistributedQueue(st_port, strategy_host)
                                    for st, st_port in strategy_ports.items()}
            print(f'[Execution] Created Strategy DistributedQueues')
        else:
            self.strategy_queues = strategy_queues

        self.logger = Logger(log_port, log_host, debug=debug)

        if backtest:
            self.portfolio = port_cls
        else:
            self.portfolio = Portfolio(execution_host=execution_host,
                                       execution_port=execution_port,
                                       execution_queue=execution_queue,
                                       strategy_host=strategy_host,
                                       strategy_ports=strategy_ports,
                                       strategy_queues=strategy_queues,
                                       log_host=log_host,
                                       log_port=log_port,
                                       redis_host=redis_host,
                                       redis_port=redis_port,
                                       redis_password=redis_password,
                                       strategy_ls=strategy_ls,
                                       backtest=backtest,
                                       debug=debug)

        self.minimum_trade_amount = MIN_TRADE_AMOUNT

        # Order Table(원장)
        self.strategy_ls = strategy_ls
        self.order_table = self.portfolio.order_table

        self.api = {
            st: CoinAPI(binance_public_key=API_KEYS[st]['binance_public'],
                        binance_private_key=API_KEYS[st]['binance_private'],
                        bybit_public_key=API_KEYS[st]['bybit_public'],
                        bybit_private_key=API_KEYS[st]['bybit_private'])
            for st in strategy_ls
        }

    # ///////////////////////////////// #
    # ==== ORDER RELATED FUNCTIONS ==== #
    # ///////////////////////////////// #

    # Backtest Func
    def exec_naive_backtest_order(self, event: OrderEvent):
        exchange = event.exchange
        asset_type = event.asset_type
        symbol = event.symbol
        quantity = event.quantity
        side = event.side
        est_fill_cost = event.est_fill_cost
        api_order_uid = 'backtest'

        fill_event = FillEvent(exchange=exchange,
                               asset_type=asset_type,
                               symbol=symbol,
                               filled_quantity=quantity,
                               order_quantity=quantity,
                               side=side,
                               fill_cost=est_fill_cost, # Todo : hoga 잔량에 따른 slippage 고려하는 Function 짜기
                               est_fill_cost=est_fill_cost,
                               api_order_uid=api_order_uid,
                               commission=None) # Commission None이면 calc_commission 수행

        self.execution_queue.put(fill_event)

    def exec_naive_pair_backtest_order(self, event: PairOrderEvent):
        self.exec_naive_backtest_order(event.first_order)
        self.exec_naive_backtest_order(event.second_order)

    def exec_order_thread(self, event: OrderEvent):
        self.logger.info('[Execution] Exec Order Thread')
        if event.direction == 'ENTRY':
            t = threading.Thread(target=self._exec_entry_order, args=(event,))
            t.start()
        elif event.direction == 'EXIT':
            t = threading.Thread(target=self._exec_exit_order, args=(event,))
            t.start()

    def exec_pair_order_thread(self, event: PairOrderEvent):
        self.logger.info('[Execution] Exec Pair Order Thread')
        t = threading.Thread(target=self._exec_pair_order, args=(event,))
        t.start()

    # ORDER FLOW(Threaded)
    def _exec_entry_order(self, event: OrderEvent):
        ot_event = self.order_table[event.strategy_id].get(event.order_uid)

        if ot_event is not None:
            ot_event.leverage_confirmed = threading.Event()
            ot_event.margin_type_confirmed = threading.Event()
            ot_event.transfer_confirmed = threading.Event()
            ot_event.order_confirmed = threading.Event()
        else:
            self.logger.error('[Execution] Order Table has no matching order: _exec_entry_order')

        # 1. Leverage Change 요청
        margin_type_confirmed, leverage_confirmed = self.entry_init_order(event)
        if margin_type_confirmed:
            ot_event.margin_type_confirmed.set()  # Set이 Wait 보다 앞에 있어야 True로 바꿔주며 wait 넘어감.
        if leverage_confirmed:
            ot_event.leverage_confirmed.set()

        ot_event.margin_type_confirmed.wait()
        ot_event.leverage_confirmed.wait()

        # 2. Transfer 요청 TODO : 추후 TransferSuccess 이벤트 구현 필요.
        transfer_success = self.entry_leverage_change(event)
        if transfer_success:  # Bybit Transfer 안하는 부분 pass
            ot_event.transfer_confirmed.set()
        ot_event.transfer_confirmed.wait()

        # 3. Order 요청
        self.entry_transfer_success(event)
        ot_event.order_confirmed.wait()

        # Order Table 에서 Event 제거
        order_success = self.order_table[event.strategy_id].pop(event.order_uid)
        self.portfolio.update_order_event_to_DB(order_success)
        self.logger.debug(f'[Execution] ORDER ENTRY SUCCESS')

        return order_success

    def _exec_exit_order(self, event: OrderEvent):
        ot_event = None
        updated = None
        for k, v in self.order_table[event.strategy_id].items():
            if k == event.order_uid:
                ot_event = self.order_table[event.strategy_id][k]
                ot_event.order_confirmed = threading.Event()
                ot_event.repay_confirmed = threading.Event()
                ot_event.transfer_confirmed = threading.Event()
                updated = True
                break

        if not updated:
            self.logger.error('[Execution] Order Table has no matching order')

        # 1. Order 요청
        self.exit_init_order(event=event)
        ot_event.order_confirmed.wait()

        # 2. Repay 요청 # TODO:: 추후 Repay success 이벤트 구현 필요하다
        repay_success = self.exit_order_success(event=event)
        if repay_success:
            ot_event.repay_confirmed.set()
        ot_event.repay_confirmed.wait()

        # 3. Transfer 요청
        transfer_success = self.exit_repay_success(event=event)
        if transfer_success:  # Bybit Transfer 안하는 부분 pass
            ot_event.transfer_confirmed.set()
        ot_event.transfer_confirmed.wait()

        # Order Table 에서 Event 제거
        order_success = self.order_table[event.strategy_id].pop(event.order_uid)
        self.portfolio.update_order_event_to_DB(order_success)
        self.logger.debug(f'[Execution] ORDER EXIT SUCCESS')

        return order_success

    def _exec_pair_order(self, event: PairOrderEvent):
        first_order = event.first_order
        second_order = event.second_order

        if first_order.direction == 'ENTRY':
            self._exec_entry_order(first_order)
            self._exec_entry_order(second_order)
            self.logger.info(f'[Execution] PAIR ENTRY SUCCESS')
        elif first_order.direction == 'EXIT':
            self._exec_exit_order(first_order)
            self._exec_exit_order(second_order)
            self.logger.info(f'[Execution] PAIR EXIT SUCCESS')

    # ENTRY PROCESS
    def entry_init_order(self, event: OrderEvent):
        self.logger.info('[Execution] (--ORDER--) ✓ Entry #1. init_order -> leverage chg')
        # Step #1: Change Leverage
        if event.asset_type == 'usdt':
            margin_type_confirmed, leverage_confirmed = self.change_leverage_and_margin_type(event)
            if margin_type_confirmed and leverage_confirmed:
                self.logger.info('[Execution] leverage, margin_type 이미 세팅 완료돼있음')
            else:
                self.logger.info('[Execution] leverage Socket Response 기다리기')
        else:
            self.logger.info('[Execution] margin은 leverage 변경이 불필요')
            margin_type_confirmed = True
            leverage_confirmed = True
        return margin_type_confirmed, leverage_confirmed

    def entry_leverage_change(self, event: OrderEvent):
        self.logger.info('[Execution] (--ORDER--) ✓ Entry #2. leverage chg -> transfer')
        # Step #2: Transfer
        successful_transfer = self.execute_transfer(event)
        return successful_transfer

    def entry_transfer_success(self, event: OrderEvent):
        self.logger.info('[Execution] (--ORDER--) ✓ Entry #3. transfer -> order')
        # Step #3: Order
        self.execute_order(event)

    # EXIT PROCESS
    def exit_init_order(self, event: OrderEvent):
        self.logger.debug(f'[Execution] (--ORDER--) ✓ Exit #1. init -> order')
        # Step #1: Order
        self.execute_order(event)

    def exit_order_success(self, event: OrderEvent):
        self.logger.debug(f'[Execution] (--ORDER--) ✓ Exit #2. order -> repay')
        successful_repay = self.execute_repay(event=event)
        return successful_repay

    def exit_repay_success(self, event: OrderEvent):
        self.logger.debug('[Execution] (--ORDER--) ✓ Exit #3. repay -> transfer')
        # Step #3: Transfer
        successful_transfer = self.execute_transfer(event)
        return successful_transfer

    # ///////////////////////////////////// #
    # ==== EXECUTION RELATED FUNCTIONS ==== #
    # ///////////////////////////////////// #

    # Executions
    def execute_order(self, event: OrderEvent):
        """
        현재 strategy에서 사용하는 event 형식에 맞춰서 개발.

        추후 좀더 format을 고려하여 형식에 맞출 필요가 있다.
        예를 들어: MKT, Market, MARKET은 모두 인식할 수 있어야 한다.
        """
        strategy_id = event.strategy_id
        exchange = event.exchange      # ex) binance, bybit
        asset_type = event.asset_type  # ex) margin, futures
        symbol = event.symbol          # ex) BTCUSDT
        order_type = event.order_type  # ex) MARKET, LIMIT, MKT, LMT
        quantity = event.quantity
        price = event.price
        side = event.side              # ex) BUY, SELL
        direction = event.direction    # ex) ENTRY, EXIT
        est_fill_cost = event.est_fill_cost

        enter_exit = None

        if order_type.lower() in ['market', 'mkt', 'm']:
            order_type = 'MARKET'

        if order_type.lower() in ['limit', 'lmt', 'l']:
            order_type = 'LIMIT'

        if direction == 'ENTRY':
            enter_exit = 'ENTER'
        elif direction == 'EXIT':
            enter_exit = 'EXIT'

        """
        현재 지원 주문 scope: USDT 선물 시장가 주문,
                           Margin 시장가 주문
        """

        # USDT 시장가 주문
        if asset_type == 'usdt' and order_type == 'MARKET':
            self.api[strategy_id].send_usdt_futures_market_order(source=exchange,
                                                                 symbol=symbol,
                                                                 side=side,
                                                                 quantity=abs(quantity),
                                                                 enter_exit=enter_exit)

        # USDT 지정가 주문
        elif asset_type == 'usdt' and order_type == 'LIMIT':
            # TODO:: LIMIT order
            pass

        # MARGIN 시장가 주문
        elif asset_type == 'margin' and order_type == 'MARKET':
            if enter_exit == 'ENTER':
                order_success = False
                order_failed_cnt = 0
                # binance.exceptions.BinanceAPIException: APIError(code=-11008): Exceeding the account's maximum borrowable limit 발생 지역
                while not order_success:
                    res = '초기값'
                    try:
                        res = self.api[strategy_id].send_isolated_margin_market_order(symbol=symbol,
                                                                                      side=side,
                                                                                      quantity=abs(quantity),
                                                                                      sideEffectType='MARGIN_BUY',
                                                                                      source='binance')

                        order_success = True
                    except:
                        print(f'[Execution] order 리턴값: {res}')
                        traceback.print_exc()
                        if order_failed_cnt == 5:
                            order_success = True

                        time.sleep(0.5)
                        order_failed_cnt += 1
                        print(f'[Execution] Retrying Isolated Margin Order: {order_failed_cnt}')

            elif enter_exit == 'EXIT':
                self.api[strategy_id].send_isolated_margin_market_order(symbol=symbol,
                                                                        side=side,
                                                                        quantity=abs(quantity),
                                                                        sideEffectType='AUTO_REPAY',
                                                                        source='binance')

        # MARGIN 지정가 주문
        elif asset_type == 'margin' and order_type == 'LIMIT':
            # TODO:: LIMIT order
            pass

    def execute_repay(self, event: OrderEvent):
        if event.asset_type == 'margin':
            # Exit 시, Order 후 바뀐 balance가 account에 반영될 때까지 시간이 소요
            # 3초나 기다려야 하지, 결국 시스템안에서 관리 필요
            self.logger.debug('[Execution] Wait and Check Repay Amount......')
            time.sleep(3)

        successful_repay = False

        if event.asset_type == 'margin':
            strategy_id = event.strategy_id
            symbol = event.symbol
            order_uid = event.order_uid
            side = event.side

            margin_acc = self.api[strategy_id].binance.get_isolated_margin_account(symbols=symbol)

            # base인 경우 total_asset 기준으로 repay를 해야 에러가 안남.
            index_price = float(margin_acc['assets'][0]['indexPrice'])
            base_total_asset_amt = float(margin_acc['assets'][0]['baseAsset']['totalAsset'])
            base_borrow_asset_amt = float(margin_acc['assets'][0]['baseAsset']['borrowed'])
            quote_borrow_amt = float(margin_acc['assets'][0]['quoteAsset']['borrowed'])

            TA = float(margin_acc['assets'][0]['baseAsset']['netAssetOfBtc'])
            TE = float(margin_acc['assets'][0]['baseAsset']['netAssetOfBtc']) + float(
                margin_acc['assets'][0]['quoteAsset']['netAssetOfBtc'])

            try:
                lev = abs(TA) / TE
                if lev < 1:
                    lev = 0
            except ZeroDivisionError:
                lev = 0

            if lev < 1:  # Position 없는 상태. 추후 레버지지 고배율(10) 이상 쓰기시작하면 문제생김
                # SHORT 진입후 BUY로 청산하는 상황 (코인 빌림)
                if side == 'BUY':
                    try:
                        if base_borrow_asset_amt != 0 and index_price * base_total_asset_amt > 1:
                            self.order_table[strategy_id][order_uid].repay_needed = base_total_asset_amt
                            res = self.api[strategy_id].binance.repay_margin(asset=symbol[:-4],
                                                                             isIsolated=True,
                                                                             symbol=symbol,
                                                                             amount=base_total_asset_amt)
                            if res['tranId'] is not None:
                                pass
                        else:
                            successful_repay = True
                            self.logger.info(f'[Execution] MARGIN Repay: Short 청산 임에도 repay 할게 없음')
                    except:
                        traceback.print_exc()

                # LONG 진입후 SELL로 청산하는 상황 (USDT 빌림)
                elif side == 'SELL':
                    if quote_borrow_amt > 0:
                        self.order_table[strategy_id][order_uid].repay_needed = quote_borrow_amt
                        self.api[strategy_id].binance.repay_margin(asset='USDT',
                                                                   isIsolated=True,
                                                                   symbol=symbol,
                                                                   amount=quote_borrow_amt)  # Auto_Repay 했는데 왜 에러 안뜨고 한번더 Repay가 되는지 의문이다. 안전장치 용도로 놔두기

                        # Auto_Repay한게 Balance에 반영되는데 시간이 오래걸리는듯. 추후 ledger랑 엮어서 시스템 내에서 처리필요
                        self.logger.error(
                            f'[Execution] MARGIN Repay: Unexpected Repay of SELL (Repay 요청은 하지만 success는 안기다리고 넘어감 Account 확인 필요) : quote_borrow_amt {quote_borrow_amt}')
                        successful_repay = True  # repay_success 안기다리고 넘어감. Long 진입 short 청산인 경우 보통 usdt 빌린건 모두 repay 처리됨. 가끔 에러로 quoute_borrow_amt 남는 것에 걸릴 바엔 자동 success 시켜버림.
                    else:
                        successful_repay = True
                        self.logger.info(
                            f'[Execution] MARGIN Repay: Clean Repay Amount No Action Needed: quote_borrow_amt {quote_borrow_amt}')
            else:
                self.logger.error(f'[Execution] margin repay check: lev > 1, still holding position?')
        else:
            successful_repay = True
            self.logger.info(f'[Execution] usdt Repay check: No Repay Needed')
        return successful_repay

    def execute_transfer(self, event: OrderEvent):
        strategy_id = event.strategy_id
        exchange = event.exchange
        asset_type = event.asset_type
        symbol = event.symbol
        amount = event.invest_amount
        direction = event.direction
        order_uid = event.order_uid

        entry_from_wallet = 'SPOT' if event.asset_type == 'margin' else 'MAIN'
        entry_to_wallet = 'ISOLATED_MARGIN' if event.asset_type == 'margin' else 'UMFUTURE'

        exit_from_wallet = 'ISOLATED_MARGIN' if event.asset_type == 'margin' else 'UMFUTURE'
        exit_to_wallet = 'SPOT' if event.asset_type == 'margin' else 'MAIN'

        if direction == 'EXIT':
            if asset_type == 'margin':
                time.sleep(3)

        successful_transfer = False

        if exchange == 'binance':
            if amount is None:
                # Fill_Event를 통해 나오는 Transfer_event인 경우에 Amount를 모름. Request 해서 재조회 필요. ENTRY, EXIT 모두 들어옴
                if asset_type == 'margin':
                    margin_acc = self.api[strategy_id].binance.get_isolated_margin_account(symbols=symbol)
                    base_borrow_amt = margin_acc['assets'][0]['baseAsset']['borrowed']
                    quote_borrow_amt = margin_acc['assets'][0]['quoteAsset']['borrowed']
                    remaining_borrowed = float(margin_acc['assets'][0]['baseAsset']['borrowed']) * float(
                        margin_acc['assets'][0]['indexPrice'])
                    quote_free_amt = int(float(
                        margin_acc['assets'][0]['quoteAsset']['free']) - remaining_borrowed * 2)  # Cent 버리기 위해 int 처리

                    # 에러 처리. 혹시나 Fill 후 Repay가 잘 안돼서 큰 Remained BTC가 남을까봐
                    if remaining_borrowed > 10:
                        self.logger.error(f'[Execution] To Large Borrowed BTC Remained: $ {remaining_borrowed}')
                        successful_transfer = False
                        return successful_transfer

                    TA = float(margin_acc['assets'][0]['baseAsset']['netAssetOfBtc'])
                    TE = float(margin_acc['assets'][0]['baseAsset']['netAssetOfBtc']) + float(
                        margin_acc['assets'][0]['quoteAsset']['netAssetOfBtc'])

                    try:
                        lev = abs(TA) / TE
                        if lev < 1:
                            lev = 0
                    except ZeroDivisionError:
                        lev = 0

                    if lev < 1:  # Position 없는 상태
                        self.order_table[event.strategy_id][order_uid].invest_amount = quote_free_amt
                        _ = self.api[strategy_id].make_wallet_transfer(source=exchange,
                                                                       from_wallet=exit_from_wallet,
                                                                       to_wallet=exit_to_wallet,
                                                                       asset='USDT',
                                                                       symbol=symbol,
                                                                       amount=quote_free_amt)

                elif event.asset_type == 'usdt':
                    # Entry Exit 구분 필요!
                    bi_usdt = self.api[strategy_id].binance.get_account('UMFUTURE')
                    for a in bi_usdt['assets']:
                        if a['asset'] == 'USDT':  # 현금
                            transfer_amt = int(float(a['availableBalance']))  # maxWithdrawAmount
                            # TODO Entry Exit 주문이 usdt에서 같이나오면 Entry 자금까지 다시 spot으로 돌려놓아버릴 가능성 있음.
                            self.order_table[event.strategy_id][order_uid].invest_amount = transfer_amt
                            _ = self.api[strategy_id].make_wallet_transfer(source=exchange,
                                                                           from_wallet=exit_from_wallet,
                                                                           to_wallet=exit_to_wallet,
                                                                           asset='USDT',
                                                                           symbol=symbol,
                                                                           amount=transfer_amt)

                else:
                    self.logger.error(f'[Execution] Incorrect Asset Type: {event.asset_type}')

            else:  # Entry Position 인 경우에 investment amount 를 통해서 여기로 들어옴!!
                _ = self.api[strategy_id].make_wallet_transfer(source=exchange,
                                                               from_wallet=entry_from_wallet,
                                                               to_wallet=entry_to_wallet,
                                                               asset='USDT',
                                                               symbol=symbol,
                                                               amount=amount)

        else:
            """
            현재 Bybit 같은 경우 usdt 마켓에서만 매매를 하기 때문에 transfer가 필요없다.
            """
            successful_transfer = True
            self.logger.info(f'[Execution] TRANSFER {exchange}: No Need to Transfer')

        return successful_transfer

    def change_leverage_and_margin_type(self, event: OrderEvent):
        strategy_id = event.strategy_id
        exchange = event.exchange
        asset_type = event.asset_type
        symbol = event.symbol
        margin_type = event.margin_type  # ISOLATED, CROSSED
        leverage = event.leverage_size

        if asset_type == 'usdt':
            # 만약 leverage와 margin_type이 바꿀 필요가 없다면 res == True 값을 리턴함.
            # api에서는 exchange가 source라고 되어 있다 --> 데이터 소스를 구분하기 위해서 사용한 parameter이기 때문
            margin_type_confirmed, leverage_confirmed = self.api[strategy_id].change_usdt_leverage(source=exchange,
                                                                                                   symbol=symbol,
                                                                                                   margin_type=margin_type,
                                                                                                   leverage=leverage)
        else:
            margin_type_confirmed = None
            leverage_confirmed = None
            self.logger.error(f'[Execution] Incorrect Asset Type for leverage change')

        return margin_type_confirmed, leverage_confirmed

    # ///////////////////////////////////// #
    # ======== CALLBACK FUNCTIONS ========= #
    # ///////////////////////////////////// #

    # Event loop callback functions (control Threading Event)
    # leverage/ transfer/ order/ repay success events
    def on_change_leverage_and_margin_type_callback(self, event: LeverageSuccessEvent or MarginTypeSuccessEvent):
        strategy_id = event.strategy_id
        for k, v in self.order_table[strategy_id].items():
            order_event = self.order_table[strategy_id][k]
            if order_event.direction == 'ENTRY':  # Exit 할때는 lev, margin 바꿔줄 필요 없다. (Bybit error debug)
                if event.type == 'LEVERAGE_SUCCESS' and not order_event.leverage_confirmed.is_set():
                    lev_matcher = f'{order_event.strategy_id}_{order_event.exchange}_{order_event.asset_type}_{order_event.symbol}_{float(order_event.leverage_size)}'
                    if event.matcher == lev_matcher:  # bybit인 경우는 LeverageSuccessEvent가 오면 둘다 잘바뀜.
                        order_event.leverage_confirmed.set()
                        self.logger.info(f'[Execution] [{event.type}] Successfully Matched')
                        break  # Order Dict의 첫번째로 매칭되는 Thread Event 만 풀어주고 Break

                if event.type == 'MARGIN_TYPE_SUCCESS' and not order_event.margin_type_confirmed.is_set():
                    margin_matcher = f'{order_event.strategy_id}_{order_event.exchange}_{order_event.asset_type}_{order_event.symbol}_{order_event.margin_type}'
                    if event.matcher == margin_matcher:
                        order_event.margin_type_confirmed.set()
                        self.logger.info(f'[Execution] [{event.type}] Successfully Matched')
                        break  # Order Dict의 첫번째로 매칭되는 Thread Event 만 풀어주고 Break

    # def on_transfer_success_callback(self, event: TransferSuccessEvent):
    #     amount = float(event.amount)
    #     amount_dir = None
    #     for st in self.strategy_ls:
    #         for k, v in self.order_table[st].items():
    #             order_event = self.order_table[st][k]
    #             if order_event.invest_amount is not None:  # Entry: invest_amount/ Exit: Quote_free_asset 이 들어있어야 한다.
    #                 symbol = None if order_event.asset_type == 'usdt' else order_event.symbol  # usdt는 transfer하는 Symbol이 None(지갑 분리 안돼있음)
    #
    #                 amount_dir = -1 if amount < 0 else 1 if amount > 0 else None  # amount가 음수면 EXIT, 각 지갑-> SPOT 으로 돈 보내주는 경우는 -1을 곱해줘야 한다.
    #                 order_matcher = f"{order_event.exchange}_{order_event.asset_type}_{symbol}_{float(amount_dir * order_event.invest_amount)}"
    #
    #                 if event.matcher == order_matcher:
    #                     order_event.transfer_confirmed.set()
    #                     self.logger.info(f"[{event.type}] Successfully Matched! {event.__dict__} @ Exec")
    #                     break
    #                 else:
    #                     self.logger.error(
    #                         f"No Matching TransferSuccess <-> Order: {event.__dict__}\n{self.order_table} @ Exec")
    #
    #     if amount_dir is None:
    #         self.logger.error(f"transfer success before transfer(margin long 주문 시 발생): {event.__dict__} @ Exec")

    # def on_order_success_callback(self, event: OrderSuccessEvent):
    #     order_event = None
    #     for st in self.strategy_ls:
    #         try:
    #             order_event = self.order_table[st][event.order_uid]
    #             order_event.order_confirmed.set()
    #             self.logger.info(f"[{event.type}] Successfully Matched! {event.__dict__} @ Exec")
    #         except KeyError:
    #             order_event = None
    #
    #     if order_event is None:
    #         self.logger.error(f"No Matching OrderSuccess <-> Order: {event.__dict__}\n{self.order_table}")

    # def on_repay_success_callback(self, event: RepaySuccessEvent):
    #     match_success = False
    #     for st in self.strategy_ls:
    #         for k, v in self.order_table[st].items():
    #             order_event = self.order_table[st][k]
    #             if order_event.repay_needed is not None:  # None이면 Repay 할 필요 없는 Order 임
    #                 symbol = order_event.symbol  # usdt는 transfer하는 Symbol이 None(지갑 분리 안돼있음)
    #                 amount_dir = -1  # repay는 Exit 할때만 발생, 항상 -1 을 곱해줘야 매칭이 됨
    #                 order_matcher = f"{order_event.exchange}_{order_event.asset_type}_{symbol}" \
    #                                 f"_{float(amount_dir * order_event.repay_needed)}"  # repay_needed는 API 조회로 넣어줌
    #
    #                 if event.matcher == order_matcher:
    #                     order_event.repay_confirmed.set()
    #                     match_success = True
    #                     self.logger.info(f"[{event.type}] Successfully Matched! {event.__dict__} @ Exec")
    #                     break
    #
    #     if not match_success:
    #         self.logger.debug(f"Unrelated Repay Event: {event.__dict__}")

    def start_execution_loop(self):
        while True:
            event = self.execution_queue.get()
            if event.type == 'JANGO' or self.portfolio.jango_updated:
                try:
                    if event.type == 'JANGO':
                        self.portfolio.update_jango(event, method='self_update')  # check position status 수행
                        self.portfolio.jango_updated = True

                    elif event.type == 'SIGNAL':
                        evt_msg = event.message(module='Execution')
                        self.logger.info(evt_msg)
                        self.portfolio.update_signal_event_to_DB(event)

                    elif event.type == 'PAIR_SIGNAL':
                        evt_msg = event.message(module='Execution')
                        self.logger.info(evt_msg)
                        self.portfolio.update_pairsignal_event_to_DB(event)

                    elif event.type == 'ORDER':
                        evt_msg = event.message(module='Execution')
                        self.logger.info(evt_msg)
                        self.portfolio.handle_order_event(event)
                        self.exec_order_thread(event)

                    elif event.type == 'PAIR_ORDER':
                        evt_msg = event.message(module='Execution')
                        self.logger.info(evt_msg)
                        self.portfolio.handle_order_event(event)
                        self.exec_pair_order_thread(event)

                    elif event.type == 'LEVERAGE_SUCCESS':
                        # self.logger.debug(f"[{event.type}] {event.__dict__} @ Exec")
                        self.on_change_leverage_and_margin_type_callback(event)

                    elif event.type == 'MARGIN_TYPE_SUCCESS':
                        # self.logger.debug(f"[{event.type}] {event.__dict__} @ Exec")
                        self.on_change_leverage_and_margin_type_callback(event)

                    # elif event.type == 'TRANSFER_SUCCESS':
                    #     self.logger.debug(f"[{event.type}] {event.__dict__} @ Exec")
                    #     self.on_transfer_success_callback(event)
                    #
                    # elif event.type == 'REPAY_SUCCESS':
                    #     self.logger.debug(f"[{event.type}] {event.__dict__} @ Exec")
                    #     self.on_repay_success_callback(event)
                    #
                    # elif event.type == 'ORDER_SUCCESS':
                    #     self.logger.debug(f"[{event.type}] {event.__dict__} @ Exec")
                    #     self.on_order_success_callback(event)

                    elif event.type == 'FILL':
                        evt_msg = event.message(module='Execution')
                        self.logger.info(evt_msg)
                        # self.portfolio.handle_fill_event(event)

                    else:
                        self.logger.error(f'[Execution] Wrong Event type: {event.type}')
                except:
                    self.logger.exception(f'[Execution] Unknown Error')
            else:
                self.logger.error(f'[Execution] Trashed Event before JANGO updated')


if __name__ == '__main__':
    from components import open_process, start_account_handler

    open_process(start_account_handler, strategy_ls=STRATEGY_LS)

    eh = ExecutionHandler(debug=True)
    eh.start_execution_loop()