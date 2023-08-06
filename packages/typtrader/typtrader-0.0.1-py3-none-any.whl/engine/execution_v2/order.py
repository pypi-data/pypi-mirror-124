import time
import datetime
import traceback
import threading
from typing import List
from multiprocessing import Queue
from cointraderkr import CoinAPI, MIN_TRADE_AMOUNT

from params import (
    API_KEYS,
    ORDER_QUEUE_HOST,
    EXAMPLE_ORDER_QUEUE_PORT,
    EXECUTION_QUEUE_HOST,
    EXECUTION_QUEUE_PORT,
)
from engine.events import (
    OrderEvent,
    PairOrderEvent,
    OrderSuccessEvent,
)
from engine.utils.log import Logger
from engine.utils.distributed_queue import DistributedQueue
from engine.execution_v2.response import CryptoResponseHandler


class CryptoOrderHandler:

    def __init__(self,
                 order_host: str = ORDER_QUEUE_HOST,
                 order_port: int = EXAMPLE_ORDER_QUEUE_PORT,
                 order_queue: Queue = None,
                 execution_host: str = EXECUTION_QUEUE_HOST,
                 execution_port: int = EXECUTION_QUEUE_PORT,
                 execution_queue: Queue = None,
                 strategy_ls: List[str] = ['example'],
                 debug: bool = False):

        self.debug = debug

        if order_queue is None:
            self.order_queue = DistributedQueue(order_port, order_host)
            print(f'[Order] Created Order DistributedQueue at tcp://{order_host}:{order_port}')
        else:
            self.order_queue = order_queue

        self.execution_host = execution_host
        self.execution_port = execution_port

        if execution_queue is None:
            self.execution_queue = DistributedQueue(execution_port, execution_host)
            print(f'[Order] Created Execution DistributedQueue at tcp://{execution_host}:{execution_port}')
        else:
            self.execution_queue = execution_queue

        self.logger = Logger(debug=debug)
        self.order_threads = {}
        self.order_thread_timeout = 20

        self.minimum_trade_amount = MIN_TRADE_AMOUNT
        self.strategy_ls = strategy_ls

        self.api = {
            st: CoinAPI(binance_public_key=API_KEYS[st]['binance_public'],
                        binance_private_key=API_KEYS[st]['binance_private'],
                        bybit_public_key=API_KEYS[st]['bybit_public'],
                        bybit_private_key=API_KEYS[st]['bybit_private'])
            for st in self.strategy_ls
        }

        self._clean_order_threads()

    def _clean_order_threads(self):
        """
        주기적으로 thread를 확인하여 종료된 thread는 제거해주는 역할

        hanging 쓰레드가 생길 수 있는데, 이를 주문 오류로 보기 위해서 order_thread_timeout 시간
        이상동안 실행된 쓰레드는 OrderFailEvent를 발생시킨다.
        """
        thread_cnt = 0
        for order_uid in list(self.order_threads.keys()):
            event = self.order_threads[order_uid]['event']
            thread = self.order_threads[order_uid]['thread']
            started = self.order_threads[order_uid]['started']
            success_event_sent = self.order_threads[order_uid]['success_event_sent']
            if not thread.is_alive():
                del self.order_threads[order_uid]
            else:
                thread_cnt += 1
                time_now = datetime.datetime.now()
                if (time_now - started).seconds >= self.order_thread_timeout:
                    if not success_event_sent:
                        order_fail_evt = OrderSuccessEvent(strategy_id=event.strategy_id,
                                                           exchange=event.exchange,
                                                           asset_type=event.asset_type,
                                                           symbol=event.symbol,
                                                           direction=event.direction,
                                                           order_uid=event.order_uid,
                                                           status='FAIL',
                                                           fail_point='socket_conn',
                                                           fail_message=f'failed to establish socket connection for {self.order_thread_timeout} seconds')
                        self.execution_queue.put(order_fail_evt)
                        del self.order_threads[order_uid]  # 오류가 발생한 쓰레드는 hanging 하더라도 삭제해준다.

        if self.debug:
            print(f'[Order] Order thread count: {thread_cnt}')

        timer = threading.Timer(10, self._clean_order_threads)
        timer.setDaemon(False)
        timer.start()

    def execute(self, event: OrderEvent or PairOrderEvent):
        event_type = event.type
        self.logger.info(f'[Order] Exec {event_type} Order Thread')

        if event_type == 'ORDER':
            if event.direction == 'ENTRY':
                order_uid = event.order_uid
                self.order_threads[order_uid] = {
                    'event': event,
                    'thread': threading.Thread(target=self._exec_entry_order,
                                               args=(event,),
                                               name=order_uid),
                    'started': datetime.datetime.now(),
                    'success_event_sent': False
                }
                self.order_threads[order_uid]['thread'].start()
            elif event.direction == 'EXIT':
                order_uid = event.order_uid
                self.order_threads[order_uid] = {
                    'event': event,
                    'thread': threading.Thread(target=self._exec_exit_order,
                                               args=(event,),
                                               name=order_uid),
                    'started': datetime.datetime.now(),
                    'success_event_sent': False
                }
                self.order_threads[order_uid]['thread'].start()

        # elif event_type == 'PAIR_ORDER':
        #     order_uid = f'{event.first_order.order_uid}_{event.second_order.order_uid}'
        #     self.order_threads[order_uid] = threading.Thread(target=self._exec_pair_order,
        #                                                      args=(event,),
        #                                                      name=order_uid)
        #     self.order_threads[order_uid].start()

    # ORDER FLOW
    def _exec_entry_order(self, event: OrderEvent):
        self.logger.info(f'[Order] Executing ::ENTRY:: order for: {event.strategy_id} {event.matcher}')

        event.leverage_confirmed = threading.Event()
        event.margin_type_confirmed = threading.Event()
        event.transfer_confirmed = threading.Event()
        event.order_confirmed = threading.Event()

        event.save()

        rh = CryptoResponseHandler(self.execution_host, self.execution_port)
        rh.start_account_stream(event, no_ws=True if event.exchange == 'bybit' else False)

        # 1. Leverage Change 요청
        margin_type_confirmed, leverage_confirmed = self.entry_init_order(event)
        if margin_type_confirmed:
            event.margin_type_confirmed.set()  # Set이 Wait 보다 앞에 있어야 True로 바꿔주며 wait 넘어감.
        if leverage_confirmed:
            event.leverage_confirmed.set()

        bybit_prev_pos = rh.check_bybit_margin_leverage()
        event.margin_type_confirmed.wait()
        event.leverage_confirmed.wait()
        event.update()

        # 2. Transfer 요청
        transfer_success = self.entry_leverage_and_margin_success(event)
        if transfer_success:  # Bybit Transfer 안하는 부분 pass
            event.transfer_confirmed.set()
        event.transfer_confirmed.wait()
        event.update()

        # 3. Order 요청
        order_id = self.entry_transfer_success(event)
        rh.check_bybit_order(order_id, bybit_prev_pos)
        event.order_confirmed.wait()
        event.update()

        if event.order_fail_point is None:
            self.logger.info(f'[Order] ENTRY ORDER SUCCESS')
            order_success_evt = OrderSuccessEvent(strategy_id=event.strategy_id,
                                                  exchange=event.exchange,
                                                  asset_type=event.asset_type,
                                                  symbol=event.symbol,
                                                  direction=event.direction,
                                                  order_uid=event.order_uid,
                                                  status='SUCCESS',
                                                  fail_point=None,
                                                  fail_message=None)
            self.execution_queue.put(order_success_evt)
        else:
            self.logger.info(f'[Order] ENTRY ORDER FAILED')
            order_fail_evt = OrderSuccessEvent(strategy_id=event.strategy_id,
                                               exchange=event.exchange,
                                               asset_type=event.asset_type,
                                               symbol=event.symbol,
                                               direction=event.direction,
                                               order_uid=event.order_uid,
                                               status='FAIL',
                                               fail_point=event.order_fail_point,
                                               fail_message=event.fail_message)
            self.execution_queue.put(order_fail_evt)

    def _exec_exit_order(self, event: OrderEvent):
        self.logger.info(f'[Order] Executing ::EXIT:: order for: {event.strategy_id} {event.matcher}')

        event.order_confirmed = threading.Event()
        event.repay_confirmed = threading.Event()
        event.transfer_confirmed = threading.Event()
        event.margin_type_confirmed = threading.Event()
        event.leverage_confirmed = threading.Event()

        event.save()

        rh = CryptoResponseHandler(self.execution_host, self.execution_port)
        rh.start_account_stream(event, no_ws=True if event.exchange == 'bybit' else False)
        bybit_prev_pos = rh.check_bybit_margin_leverage()

        # 1. Order 요청
        order_id = self.exit_init_order(event)
        rh.check_bybit_order(order_id, bybit_prev_pos)
        event.order_confirmed.wait()
        event.update()

        # 2. Repay 요청
        repay_success = self.exit_order_success(event)
        if repay_success:
            event.repay_confirmed.set()
        event.repay_confirmed.wait()
        event.update()

        # 3. Transfer 요청
        transfer_success = self.exit_repay_success(event)
        if transfer_success:  # Bybit Transfer 안하는 부분 pass
            event.transfer_confirmed.set()
        event.transfer_confirmed.wait()
        event.update()

        if event.order_fail_point is None:
            self.logger.info(f'[Order] EXIT ORDER SUCCESS')
            order_success_evt = OrderSuccessEvent(strategy_id=event.strategy_id,
                                                  exchange=event.exchange,
                                                  asset_type=event.asset_type,
                                                  symbol=event.symbol,
                                                  direction=event.direction,
                                                  order_uid=event.order_uid,
                                                  status='SUCCESS',
                                                  fail_point=None,
                                                  fail_message=None)
            self.execution_queue.put(order_success_evt)
        else:
            self.logger.info(f'[Order] EXIT ORDER FAILED')
            order_fail_evt = OrderSuccessEvent(strategy_id=event.strategy_id,
                                               exchange=event.exchange,
                                               asset_type=event.asset_type,
                                               symbol=event.symbol,
                                               direction=event.direction,
                                               order_uid=event.order_uid,
                                               status='FAIL',
                                               fail_point=event.order_fail_point,
                                               fail_message=event.fail_message)
            self.execution_queue.put(order_fail_evt)

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
        self.logger.info('[Order] (--ORDER--) Entry #1. init_order -> leverage chg')
        # Step #1: Change Leverage
        if event.asset_type == 'usdt':
            margin_type_confirmed, leverage_confirmed = self.change_leverage_and_margin_type(event)
            if margin_type_confirmed and leverage_confirmed:
                self.logger.info('[Order] leverage, margin_type 이미 세팅 완료돼있음')
            else:
                self.logger.info('[Order] leverage Socket Response 기다리기')
        else:
            self.logger.info('[Order] margin은 leverage 변경이 불필요')
            margin_type_confirmed = True
            leverage_confirmed = True
        return margin_type_confirmed, leverage_confirmed

    def entry_leverage_and_margin_success(self, event: OrderEvent):
        self.logger.info('[Order] (--ORDER--) Entry #2. leverage chg -> transfer')
        # Step #2: Transfer
        successful_transfer = self.execute_transfer(event)
        return successful_transfer

    def entry_transfer_success(self, event: OrderEvent):
        self.logger.info('[Order] (--ORDER--) Entry #3. transfer -> order')
        # Step #3: Order
        return self.execute_order(event)

    # EXIT PROCESS
    def exit_init_order(self, event: OrderEvent):
        self.logger.debug(f'[Order] (--ORDER--) Exit #1. init -> order')
        # Step #1: Order
        return self.execute_order(event)

    def exit_order_success(self, event: OrderEvent):
        self.logger.debug(f'[Order] (--ORDER--) Exit #2. order -> repay')
        successful_repay = self.execute_repay(event)
        return successful_repay

    def exit_repay_success(self, event: OrderEvent):
        self.logger.debug('[Order] (--ORDER--) Exit #3. repay -> transfer')
        # Step #3: Transfer
        successful_transfer = self.execute_transfer(event)
        return successful_transfer

    # ///////////////////////////////////// #
    # ==== EXECUTION RELATED FUNCTIONS ==== #
    # ///////////////////////////////////// #
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
            self.logger.error(f'[Order] Incorrect Asset Type for leverage change')

        return margin_type_confirmed, leverage_confirmed

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
                        self.logger.error(f'[Order] To Large Borrowed BTC Remained: $ {remaining_borrowed}')
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
                        event.invest_amount = quote_free_amt
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
                            event.invest_amount = transfer_amt
                            _ = self.api[strategy_id].make_wallet_transfer(source=exchange,
                                                                           from_wallet=exit_from_wallet,
                                                                           to_wallet=exit_to_wallet,
                                                                           asset='USDT',
                                                                           symbol=symbol,
                                                                           amount=transfer_amt)

                else:
                    self.logger.error(f'[Order] Incorrect Asset Type: {event.asset_type}')

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
            self.logger.info(f'[Order] TRANSFER {exchange}: No Need to Transfer')

        return successful_transfer

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
            res = self.api[strategy_id].send_usdt_futures_market_order(source=exchange,
                                                                       symbol=symbol,
                                                                       side=side,
                                                                       quantity=abs(quantity),
                                                                       enter_exit=enter_exit)
            if exchange == 'bybit':
                order_id = res[0]['result']['order_id']
                return order_id

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
                        print(f'[Order] order 리턴값: {res}')
                        traceback.print_exc()
                        if order_failed_cnt == 5:
                            order_success = True

                        time.sleep(0.5)
                        order_failed_cnt += 1
                        print(f'[Order] Retrying Isolated Margin Order: {order_failed_cnt}')

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
            # 3초나 기다려야 한다. 결국 시스템안에서 관리 필요
            self.logger.debug('[Order] Wait and Check Repay Amount. Sleeping 3 seconds')
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
                            event.repay_needed = base_total_asset_amt
                            res = self.api[strategy_id].binance.repay_margin(asset=symbol[:-4],
                                                                             isIsolated=True,
                                                                             symbol=symbol,
                                                                             amount=base_total_asset_amt)
                            if res['tranId'] is not None:
                                pass
                        else:
                            successful_repay = True
                            self.logger.info(f'[Order] MARGIN Repay: Short 청산 임에도 repay 할게 없음')
                    except:
                        traceback.print_exc()

                # LONG 진입후 SELL로 청산하는 상황 (USDT 빌림)
                elif side == 'SELL':
                    if quote_borrow_amt > 0:
                        event.repay_needed = quote_borrow_amt
                        self.api[strategy_id].binance.repay_margin(asset='USDT',
                                                                   isIsolated=True,
                                                                   symbol=symbol,
                                                                   amount=quote_borrow_amt)  # Auto_Repay 했는데 왜 에러 안뜨고 한번더 Repay가 되는지 의문이다. 안전장치 용도로 놔두기

                        # Auto_Repay한게 Balance에 반영되는데 시간이 오래걸리는듯. 추후 ledger랑 엮어서 시스템 내에서 처리필요
                        self.logger.error(
                            f'[Order] MARGIN Repay: Unexpected Repay of SELL (Repay 요청은 하지만 success는 안기다리고 넘어감 Account 확인 필요) : quote_borrow_amt {quote_borrow_amt}')
                        successful_repay = True  # repay_success 안기다리고 넘어감. Long 진입 short 청산인 경우 보통 usdt 빌린건 모두 repay 처리됨. 가끔 에러로 quoute_borrow_amt 남는 것에 걸릴 바엔 자동 success 시켜버림.
                    else:
                        successful_repay = True
                        self.logger.info(
                            f'[Order] MARGIN Repay: Clean Repay Amount No Action Needed: quote_borrow_amt {quote_borrow_amt}')
            else:
                self.logger.error(f'[Order] margin repay check: lev > 1, still holding position?')
        else:
            # repay는 binance margin에서만 사용
            successful_repay = True
            self.logger.info(f'[Order] Repay check: No Repay Needed')
        return successful_repay

    def start_order_loop(self):
        while True:
            event = self.order_queue.get()

            if event.type == 'ORDER':
                self.execute(event)

            elif event.type == 'PAIR_ORDER':
                self.execute(event)


if __name__ == '__main__':
    # from engine.events import SignalEvent
    #
    # logger = Logger(debug=True)
    #
    # strategy_ls = ['example']
    # order_table = {st: OrderedDict() for st in strategy_ls}
    #
    # sig_evt = SignalEvent(strategy_id='example',
    #                       symbol='DOGEUSDT',
    #                       exchange='bybit',
    #                       asset_type='usdt',
    #                       signal_type='ENTRY',
    #                       signal_price=0.3,
    #                       order_type='MKT')
    #
    # ord_evt = OrderEvent(strategy_id='example',
    #                      exchange='bybit',
    #                      asset_type='usdt',
    #                      symbol='DOGEUSDT',
    #                      order_type='MKT',
    #                      quantity=50,
    #                      price=None,
    #                      side='BUY',
    #                      direction='ENTRY',
    #                      leverage_size=1,
    #                      invest_amount=0.3 * 50,
    #                      margin_type='ISOLATED',
    #                      est_fill_cost=0,
    #                      signal_uid=sig_evt.signal_uid,
    #                      paired=False)
    #
    # order_table['example'][ord_evt.order_uid] = ord_evt
    #
    # handler = CryptoOrderHandler(logger, order_table)
    # handler._exec_entry_order(ord_evt)

    oh = CryptoOrderHandler(order_port=1111, debug=True)
    oh.start_order_loop()