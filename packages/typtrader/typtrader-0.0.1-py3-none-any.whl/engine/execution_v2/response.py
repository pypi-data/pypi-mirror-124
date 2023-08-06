import time
import datetime
import traceback
import threading
from decimal import Decimal
from cointraderkr import (
    BybitWebsocket,
    BinanceBulkWebsocket,
    BinanceAPI,
    CoinAPI,
)
from multiprocessing import Queue

from params import (
    API_KEYS,
    EXECUTION_QUEUE_HOST,
    EXECUTION_QUEUE_PORT,
)
from engine.events import OrderEvent, FillEvent
from engine.utils.distributed_queue import DistributedQueue


class CryptoResponseHandler:
    """
    총 사용 쓰레드 수: 3개
    - Order의 상태를 트래킹하는 쓰레드 (daemon)
    - account stream을 받는 웹소켓 쓰레드 (daemon)
    - 바이비트 전용 ping 쓰레드 (daemon)
    """

    event = None
    stop_order = None
    order_start_time = None

    def __init__(self,
                 execution_host: str = EXECUTION_QUEUE_HOST,
                 execution_port: int = EXECUTION_QUEUE_PORT,
                 execution_queue: Queue = None):

        if execution_queue is None:
            self.execution_queue = DistributedQueue(execution_port, execution_host)
        else:
            self.execution_queue = execution_queue

        self.fail_timeout = 15        # 소켓 연결을 하고 15초동안 response를 못 받는 경우 오류로 핸들링

        self.binance_ws: BinanceBulkWebsocket or None = None
        self.bybit_ws: BybitWebsocket or None = None
        self.bybit_api: CoinAPI or None = None

        self.bybit_sub_complete = {'position': False, 'execution': False}

    @property
    def bybit_ready(self):
        if self.bybit_ws is not None:
            return all(self.bybit_sub_complete.values())
        elif self.binance_ws is not None:
            return True

    def check_bybit_margin_leverage(self):
        if self.bybit_api is not None:
            self.order_start_time = datetime.datetime.now()
            res = self.bybit_api.bybit.get_usdt_futures_positions(symbol=self.event.symbol)
            r = res[0] if self.event.side == 'BUY' else res[1]
            bybit_prev_pos = {
                'init_lev': float(r['leverage']),
                'init_margin': float(r['position_margin']),
                'init_size': float(r['size'])
            }
            margin_type = r.get('is_isolated')
            if margin_type:
                margin_type = 'ISOLATED'
            else:
                margin_type = 'CROSSED'
            leverage = float(r.get('leverage'))
            if self.event.margin_type == margin_type:
                self.event.margin_type_confirmed.set()
            if float(self.event.leverage_size) == leverage:
                self.event.leverage_confirmed.set()
            return bybit_prev_pos

    def check_bybit_order(self, order_id: str, bybit_prev_pos: dict):
        if self.bybit_api is not None:
            remaining_quantity = None
            while remaining_quantity != 0:
                self.order_start_time = datetime.datetime.now()
                res = self.bybit_api.bybit.get_usdt_futures_positions(symbol=self.event.symbol)
                r = res[0] if self.event.side == 'BUY' else res[1]
                curr_lev = float(r['leverage'])
                curr_margin = float(r['position_margin'])
                curr_size = float(r['size'])

                size_change = abs(curr_size - bybit_prev_pos['init_size'])
                value_change = abs((curr_lev * curr_margin) - (bybit_prev_pos['init_lev'] * bybit_prev_pos['init_margin']))
                avg_prc = value_change / size_change

                if remaining_quantity is None:
                    remaining_quantity = self.event.remaining_quantity

                remaining_quantity -= size_change

                """
                remaining_quantity를 주기적으로 확인하면서 완전히 fill된 경우에만 fill_check로 res_data를 보내준다.
                만약 완전 fill이 안 된 상태라면 0.5초를 쉰 다음 다시 api요청을 보내본다.
                """
                if remaining_quantity != 0:
                    time.sleep(0.2)
                else:
                    # https://learn.bybit.com/bybit-guide/bybit-trading-fees/
                    order_type = self.event.order_type
                    if order_type.upper()[0] == 'M':
                        order_type = 'MKT'
                    elif order_type.upper()[0] == 'L':
                        order_type = 'LMT'
                    is_maker = True if order_type == 'LMT' else False
                    fee_pct = 0.00075 if not is_maker else 0
                    commission = size_change * avg_prc * fee_pct

                    res_data = {
                        'filled_quantity': size_change,
                        'order_quantity': self.event.quantity,
                        'fill_price': avg_prc,
                        'order_price': None,
                        'api_order_uid': order_id,
                        'commission': commission
                    }

                    self.fill_check(res_data)

    def start_account_stream(self, event: OrderEvent = None, no_ws: bool = False):
        self.event = event
        self.stop_order = False
        self.order_start_time = datetime.datetime.now()

        strategy_id = self.event.strategy_id
        exchange = self.event.exchange
        asset_type = self.event.asset_type

        if exchange == 'binance':
            public_key = API_KEYS[strategy_id]['binance_public']
            private_key = API_KEYS[strategy_id]['binance_private']

            self.binance_ws = BinanceBulkWebsocket(public_key=public_key,
                                                   secret_key=private_key,
                                                   symbol=self.event.symbol,
                                                   callback=self.account_data_callback)
            self.binance_ws.start()

        elif exchange == 'bybit' and not no_ws:
            public_key = API_KEYS[strategy_id]['bybit_public']
            private_key = API_KEYS[strategy_id]['bybit_private']

            if asset_type == 'usdt':
                url = 'wss://stream.bytick.com/realtime_private'
                self.bybit_ws = BybitWebsocket(wsURL=url,
                                               api_key=public_key,
                                               api_secret=private_key,
                                               callback=self.account_data_callback)
                self.bybit_ws.subscribe_position()
                self.bybit_ws.subscribe_execution()
                # self.bybit_ws.subscribe_order()
                # self.bybit_ws.subscribe_stop_order()
                # self.bybit_ws.subscribe_wallet()

                # Bybit 웹소켓은 주기적으로 핑을 보내주지 않으면 연결이 끊긴다.
                self._ping_loop()

        # 웹소켓을 사용하지 않는 경우
        # --> Connection is already closed 문제가 자주 발생하여 매우 불안정적인 관계로 Rest 기반도 마련
        elif exchange == 'bybit' and no_ws:
            self.bybit_api = CoinAPI(binance_public_key=API_KEYS[strategy_id]['binance_public'],
                                     binance_private_key=API_KEYS[strategy_id]['binance_private'],
                                     bybit_public_key=API_KEYS[strategy_id]['bybit_public'],
                                     bybit_private_key=API_KEYS[strategy_id]['bybit_private'])

        self._check_order_status()

    def _check_order_status(self):
        if self.order_start_time is not None and not self.stop_order:
            time_now = datetime.datetime.now()
            if (time_now - self.order_start_time).seconds >= self.fail_timeout:
                """
                ENTRY, EXIT을 구분하여 현재 에러가 발생한 지점 (현재 실행 부분) 을 발견한다.
                그리고 강제로 모든 스텝들을 set 시켜준다. (thread exit 강제화하기)
                """
                try:
                    """
                    강제로 이벤트를 종료시킴으로써 wait()를 모두 통과시키는 것이 목적
                    추가로 이러한 경우 주문을 넣으면서 문제가 발생한 것이기 때문에 order_fail_point를 설정해준다.
                    """
                    if self.event.direction == 'ENTRY':
                        self.event.order_fail_point = self.event.crypto_entry_curr_step
                        if self.event.order_fail_point is not None:
                            steps_start_idx = self.event.crypto_entry_steps.index(self.event.order_fail_point)
                            steps_list = self.event.crypto_entry_steps[steps_start_idx:]
                            for step in steps_list:
                                getattr(self.event, f'{step}_confirmed').set()

                    elif self.event.direction == 'EXIT':
                        self.event.order_fail_point = self.event.crypto_exit_curr_step
                        if self.event.order_fail_point is not None:
                            steps_start_idx = self.event.crypto_exit_steps.index(self.event.order_fail_point)
                            steps_list = self.event.crypto_exit_steps[steps_start_idx:]
                            for step in steps_list:
                                getattr(self.event, f'{step}_confirmed').set()
                    print(f'{self.event.matcher} Order failed at: {self.event.order_fail_point}')
                except:
                    traceback.print_exc()

                # 오류로 인한 종료
                self.event.order_status = False
                self.stop_order = True
                self.order_start_time = None
                self.stop_account_stream()

            """
            1초를 주기로 order가 중단되지는 않았는지 확인한다.
            daemon을 True로 하여 thread 내에서도 실행이 되도록 한다.
            """
            timer = threading.Timer(1, self._check_order_status)
            timer.setDaemon(True)
            timer.start()

    def stop_account_stream(self):
        if self.binance_ws is not None:
            self.binance_ws.stop()
            self.binance_ws = None

        if self.bybit_ws is not None:
            self.bybit_ws.exit()
            self.bybit_ws = None

    def _ping_loop(self):
        if self.bybit_ws is not None:
            self.bybit_ws.ping()

            timer = threading.Timer(5, self._ping_loop)
            timer.setDaemon(True)
            timer.start()

    def response_data_mapper(self, data: dict) -> (str, dict):
        res_type = None
        res_data = {}

        if data['source'] == 'binance':
            if data['type'] == 'usdt_futures_account':

                if data['e'] == 'ACCOUNT_CONFIG_UPDATE':
                    res_type = 'LEVERAGE_CHANGE'
                    res_data['leverage_size'] = int(data['ac']['l'])

                elif data['e'] == 'ACCOUNT_UPDATE':
                    if data['a']['m'] == 'MARGIN_TYPE_CHANGE':
                        res_type = 'MARGIN_CHANGE'
                        margin_type = data['a']['P'][0]['mt']
                        if margin_type == 'cross':
                            margin_type = 'crossed'
                        res_data['margin_type'] = margin_type

                    elif data['a']['m'] == 'DEPOSIT' or data['a']['m'] == 'WITHDRAW':
                        res_type = 'TRANSFER'
                        res_data['transferred'] = float(data['a']['B'][0]['bc'])

                elif data['e'] == 'ORDER_TRADE_UPDATE':
                    res_type = 'FILL'
                    res_data = {
                        'status': data['o']['X'],                    # NEW, FILLED, PARTIALLY_FILLED
                        'symbol': data['o']['s'],
                        'side': data['o']['S'],
                        'order_quantity': float(data['o']['q']),     # 주문수량
                        'filled_quantity': float(data['o']['l']),      # 체결수량
                        'cum_fill_quantity': float(data['o']['z']),  # 누적 체결수량 앞서 체결된 partially_filled 까지 다 포함해서 해당 오더에 대한 전체 체결 수량
                        'order_price': float(data['o']['ap']),       # 주문가격
                        'fill_price': float(data['o']['L']),         # 체결가격
                        'api_order_uid': data['o']['c'],
                        'commission': float(data['o'].get('n', 0)),  # 수수료
                     }

            elif data['type'] == 'isolated_margin_account':
                pass

        elif data['source'] == 'bybit':
            if data.get('asset_type') == 'usdt':

                if data['type'] == 'position':
                    if len(data['data']) == 2:  # length가 1개인 position msg 도 돌아옴, 주문체결될때.
                        if data['data'][0]['size'] == 0 and data['data'][1]['size'] == 0:
                            long_lev = float(data['data'][0]['leverage'])
                            short_lev = float(data['data'][1]['leverage'])

                            if long_lev != short_lev:
                                print(f'[Response] Bybit leverage unmatched: {long_lev} != {short_lev}')

                            res_type = 'LEVERAGE_MARGIN_CHANGE'
                            res_data = {
                                'leverage_size': long_lev,
                                'margin_type': 'crossed' if long_lev == 100 else 'isolated'
                            }

                elif data['type'] == 'execution':
                    filled_quantity = 0
                    commission = 0
                    weighted_fill_price = 0

                    symbol = None
                    side = None
                    order_quantity = None
                    exec_quantity = None
                    order_price = None
                    avg_fill_price = None
                    api_order_uid = None

                    for i in range(len(data['data'])):
                        symbol = data['data'][i]['symbol']
                        side = data['data'][i]['side'].upper()
                        order_quantity = float(data['data'][i]['order_qty'])
                        exec_quantity = Decimal(str(data['data'][i]['exec_qty']))
                        filled_quantity += exec_quantity  # 체결수량 (A)
                        order_price = None  # 주문가격, 현재 fill_price로 쓰는 price가 order_price 일수도 있음 추후 확인필요.
                        weighted_fill_price += float(data['data'][i]['price']) * float(exec_quantity)  # 체결가격 가중 합 (B)
                        avg_fill_price = weighted_fill_price / float(filled_quantity)  # 체결가격 가중평균 (B/A)
                        commission += float(data['data'][i]['exec_fee'])  # 수수료
                        api_order_uid = data['data'][i]['order_id']

                    res_type = 'FILL'
                    res_data = {
                        'status': 'FILLED',
                        'symbol': symbol,
                        'side': side,
                        'order_quantity': order_quantity,
                        'exec_quantity': exec_quantity,
                        'filled_quantity': float(filled_quantity),
                        'order_price': order_price,
                        'fill_price': avg_fill_price,
                        'api_order_uid': api_order_uid,
                        'commission': commission,
                    }

        return res_type, res_data

    def account_data_callback(self, data: dict):
        if data['source'] == 'bybit' and 'conn_id' in data:
            req = data.get('request', {})
            if req.get('op') == 'subscribe':
                args = req.get('args')[0]
                self.bybit_sub_complete[args] = True

        res_type, res_data = self.response_data_mapper(data)

        if res_type == 'LEVERAGE_CHANGE':
            self.leverage_change_check(res_data)
        elif res_type == 'MARGIN_CHANGE':
            self.margin_change_check(res_data)
        elif res_type == 'LEVERAGE_MARGIN_CHANGE':
            self.leverage_change_check(res_data)
            self.margin_change_check(res_data)
        elif res_type == 'TRANSFER':
            self.transfer_check(res_data)
        elif res_type == 'FILL':
            self.fill_check(res_data)

    # order_start_time을 매번 업데이트를 해주어 order stop 타임아웃 시간을 초기화시켜준다.
    def leverage_change_check(self, res_data: dict):
        self.order_start_time = datetime.datetime.now()
        if res_data['leverage_size'] == int(self.event.leverage_size):
            self.event.leverage_confirmed.set()

    def margin_change_check(self, res_data: dict):
        self.order_start_time = datetime.datetime.now()
        if res_data['margin_type'] == self.event.margin_type.lower():
            self.event.margin_type_confirmed.set()

    def transfer_check(self, res_data: dict):
        self.order_start_time = datetime.datetime.now()
        entry_condition = self.event.direction == 'ENTRY' and res_data['transferred'] == float(self.event.invest_amount)
        exit_condition = self.event.direction == 'EXIT'
        if entry_condition or exit_condition:
            if self.event.direction == 'EXIT':
                self.event.order_status = True  # 성공적으로 주문을 마친 경우
                self.stop_order = True
                self.order_start_time = None
                self.stop_account_stream()
            self.event.transfer_confirmed.set()

    def fill_check(self, res_data: dict):
        """
        Fill은 여러 차례에 걸쳐서 처리될 수 있기 때문에 FillEvent를 ExecutionHandler로 보낸다.
        ExecutionHandler에서는 FillEvent를 Portfolio로 보내어 핸들링한다.

        event의 order_confirmed는 Portfolio에서 이뤄진다.
        """
        self.order_start_time = datetime.datetime.now()

        filled_quantity = res_data['filled_quantity']
        order_quantity = res_data['order_quantity']
        fill_price = res_data['fill_price']
        order_price = res_data['order_price']
        api_order_uid = res_data['api_order_uid']
        commission = res_data['commission']

        # OrderEvent 업데이트
        if self.event.api_order_uid is None:
            self.event.api_order_uid = api_order_uid
            self.event.remaining_quantity = float(Decimal(str(self.event.quantity)) - Decimal(str(filled_quantity)))
        else:
            self.event.remaining_quantity = float(Decimal(str(self.event.remaining_quantity)) - Decimal(str(filled_quantity)))

        if self.event.remaining_quantity == 0:
            status = 'FILLED'
            self.event.status = 'FILLED'
        else:
            status = 'PARTIALLY_FILLED'
            self.event.status = 'PARTIALLY_FILLED'

        # FillEvent 발생
        fill_event = FillEvent(strategy_id=self.event.strategy_id,
                               exchange=self.event.exchange,
                               asset_type=self.event.asset_type,
                               symbol=self.event.symbol,
                               side=self.event.side,
                               direction=self.event.direction,
                               filled_quantity=filled_quantity,
                               order_quantity=order_quantity,
                               fill_cost=filled_quantity * fill_price,
                               est_fill_cost=None if order_price is None else order_quantity * order_price,
                               api_order_uid=api_order_uid,
                               order_uid=self.event.order_uid,
                               signal_uid=self.event.signal_uid,
                               commission=commission)

        if status == 'FILLED':
            print(f'Filled order: {self.event.matcher}')
            self.execution_queue.put(fill_event)
            if self.event.direction == 'ENTRY' or self.event.exchange == 'bybit':
                """
                Bybit같은 경우 exit 주문에 repay, transfer를 하지 않기 때문에 order만 확인하고 소켓 연결을 끊는다.
                """
                self.event.order_status = True  # 성공적으로 주문을 마친 경우
                self.stop_order = True
                self.order_start_time = None
                self.stop_account_stream()
            self.event.order_confirmed.set()

        elif status == 'PARTIALLY_FILLED':
            print(f'Partially filled order: {self.event.matcher}')
            self.execution_queue.put(fill_event)

        elif res_data['status'] == 'NEW':
            pass


if __name__ == '__main__':
    import time
    from engine.events import SignalEvent

    sig_evt = SignalEvent(strategy_id='example',
                          exchange='bybit',
                          asset_type='usdt',
                          symbol='DOGEUSDT',
                          signal_type='ENTRY',
                          signal_price=0.3,
                          order_type='MKT')

    ord_evt = OrderEvent(strategy_id='example',
                         exchange='bybit',
                         asset_type='usdt',
                         symbol='DOGEUSDT',
                         order_type='MKT',
                         quantity=10,
                         price=None,
                         side='BUY',
                         direction='ENTRY',
                         leverage_size=1,
                         invest_amount=0.3 * 50,
                         margin_type='ISOLATED',
                         est_fill_cost=0,
                         signal_uid=sig_evt.signal_uid,
                         paired=False)

    handler = CryptoResponseHandler()
    handler.start_account_stream(ord_evt)

    while True:
        pass

    # public_key = API_KEYS['example']['binance_public']
    # private_key = API_KEYS['example']['binance_private']
    # binance_api = BinanceAPI(public_key, private_key)
    #
    # cnt = 1
    #
    # while True:
    #     time.sleep(1)
    #     cnt += 1
    #     binance_api.change_usdt_futures_leverage('ETHUSDT', cnt)
    #     if cnt == 5:
    #         break
    #
    # # handler.stop_account_stream()
    #
    # binance_api.change_usdt_futures_leverage('ETHUSDT', 1)
    #
    # binance_api.transfer_isolated_margin_account(from_wallet='SPOT',
    #                                              to_wallet='ISOLATED_MARGIN',
    #                                              asset='USDT',
    #                                              symbol='ETHUSDT',
    #                                              amount=10)
    # binance_api.transfer_isolated_margin_account(from_wallet='ISOLATED_MARGIN',
    #                                              to_wallet='SPOT',
    #                                              asset='USDT',
    #                                              symbol='ETHUSDT',
    #                                              amount=10)
    #
    # while True:
    #     time.sleep(10)
    #     break