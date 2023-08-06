import os
import hashlib
import threading
from typing import List
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
application = get_wsgi_application()

from db.models import Order
from engine.events.event import Event


class OrderEvent(Event):

    def __init__(self,
                 strategy_id: str,
                 exchange: str,
                 asset_type: str,
                 symbol: str,
                 order_type: str,
                 quantity: int or float,
                 price: int or float,
                 side: str,
                 direction: str,
                 leverage_size: int or float,
                 margin_type: str,
                 invest_amount: int or float,
                 signal_uid: str,
                 paired: bool = False,
                 est_fill_cost: int or float = None,

                 status: str = None,
                 api_order_uid: str = None,
                 remaining_quantity: int or float = None,
                 log_time: str = None,
                 order_uid: str = None,
                 leverage_confirmed: bool = None,
                 margin_type_confirmed: bool = None,
                 transfer_confirmed: bool = None,
                 order_confirmed: bool = None,
                 repay_confirmed: bool = None,
                 repay_needed: bool = None,

                 order_status: bool = False,
                 order_fail_point: str = None,
                 fail_message: str = None,

                 retry: bool = None,
                 retry_num: int = None,
                 retry_cnt: int = None,
                 **kwargs):

        self.type = 'ORDER'
        self.strategy_id = strategy_id
        self.exchange = exchange.lower()  # binance, bybit
        self.asset_type = asset_type.lower()  # usdt, coinm, spot, margin
        self.symbol = symbol.upper()
        self.order_type = order_type.upper()  # MKT, LMT
        self.quantity = quantity  # 모든 Quantity는 양수로 통일함
        self.price = price
        self.side = side.upper()  # BUY, SELL
        self.direction = direction.upper()  # ENTRY, EXIT
        self.leverage_size = leverage_size
        self.margin_type = margin_type.upper()  # ISOLATED, CROSSED
        self.invest_amount = invest_amount  # Transfer Amount로도 쓰인다. Exit 시에는 Api에서 조회된 Quote_free_asset 같은게 들어감. 추후 Transfer_Asset으로 따로 구분해도 좋을듯
        self.signal_uid = signal_uid
        self.paired = paired  # Exec에서 OrderSuccess Event 낼때 사용
        self.est_fill_cost = est_fill_cost
        self.matcher = f'{self.exchange}_{self.asset_type}_{self.symbol}_{self.side}_{str(float(self.quantity))}'

        self.status = 'INIT' if status is None else status
        self.api_order_uid = None if api_order_uid is None else api_order_uid
        self.remaining_quantity = quantity if remaining_quantity is None else remaining_quantity
        self.log_time = self._time() if log_time is None else log_time
        self.order_uid = self._make_unique_id() if order_uid is None else order_uid

        # Order 주문처리 check variables
        # execution에서 threading.Event로 넣어주기
        self.leverage_confirmed = False if leverage_confirmed is None else leverage_confirmed
        self.margin_type_confirmed = False if margin_type_confirmed is None else margin_type_confirmed
        self.transfer_confirmed = False if transfer_confirmed is None else transfer_confirmed
        self.order_confirmed = False if order_confirmed is None else order_confirmed
        self.repay_confirmed = False if repay_confirmed is None else repay_confirmed

        self.repay_needed = None if repay_needed is None else repay_needed  # Repay 할필요 없으면 None 값으로 옴.

        self.order_status = False if order_status is None else order_status
        self.order_fail_point = None if order_fail_point is None else order_fail_point
        self.fail_message = None if fail_message is None else fail_message

        self.retry = False if retry is None else retry
        self.retry_num = 0 if retry_num is None else retry_num
        self.retry_cnt = 0 if retry_cnt is None else retry_cnt

        self.db_inst = None

    # order_table의 키 값으로 사용.
    def _make_unique_id(self):
        string = f'{self.strategy_id}_{self.exchange}_{self.asset_type}_{self.symbol}' \
                 f'_{self.quantity}_{self.order_type}_{self.side}_{self.log_time}'
        encoded_str = string.encode('utf-8')
        sha_string = hashlib.sha1(encoded_str).hexdigest()
        return sha_string

    def print_order(self):
        print('Order: Symbols=%s, Type=%s, Quantity=%s, Direction=%s, est_Fill_Cost=%s, exchange=%s' %
              (self.symbol, self.order_type, self.quantity, self.direction, self.est_fill_cost, self.exchange))

    def message(self, module: str):
        return f'[{module}]\n' \
               f'--- Type: {self.type} ---\n' \
               f'Strategy ID: {self.strategy_id}\n' \
               f'{self.exchange} {self.asset_type} {self.symbol}\n' \
               f'{self.order_type} {self.side} {self.direction}\n' \
               f'Price: {self.price}, Quantity: {self.quantity}\n' \
               f'Margin: {self.margin_type}, Leverage: {self.leverage_size}'

    def json(self) -> dict:
        json_data = {}
        for key, val in self.__dict__.items():
            if key != 'db_inst':
                if type(val) == threading.Event:
                    json_data[key] = val.is_set()
                else:
                    json_data[key] = val
        return json_data

    @property
    def crypto_entry_steps(self) -> List[str]:
        return ['margin_type', 'leverage', 'transfer', 'order']

    @property
    def crypto_exit_steps(self) -> List[str]:
        return ['order', 'repay', 'transfer']

    @property
    def crypto_entry_done(self) -> bool:
        steps_confirmed = []
        for step in self.crypto_entry_steps:
            confirmed = getattr(self, f'{step}_confirmed')
            if type(confirmed) == threading.Event:
                confirmed = confirmed.is_set()
            steps_confirmed.append(confirmed)
        return all(steps_confirmed)

    @property
    def crypto_entry_curr_step(self) -> str or None:
        for step in self.crypto_entry_steps:
            confirmed = getattr(self, f'{step}_confirmed')
            if type(confirmed) == threading.Event:
                confirmed = confirmed.is_set()
            if not confirmed:
                return step
        return None

    @property
    def crypto_exit_done(self) -> bool:
        steps_confirmed = []
        for step in self.crypto_exit_steps:
            confirmed = getattr(self, f'{step}_confirmed')
            if type(confirmed) == threading.Event:
                confirmed = confirmed.is_set()
            steps_confirmed.append(confirmed)
        return all(steps_confirmed)

    @property
    def crypto_exit_curr_step(self) -> str or None:
        for step in self.crypto_exit_steps:
            confirmed = getattr(self, f'{step}_confirmed')
            if type(confirmed) == threading.Event:
                confirmed = confirmed.is_set()
            if not confirmed:
                return step
        return None

    def save(self):
        self.db_inst = Order(**self.json())
        return self.db_inst.stream_save()

    def update(self):
        return self.db_inst.stream_update(**self.json())


if __name__ == '__main__':
    ord_evt = OrderEvent(strategy_id='example',
                         exchange='bybit',
                         asset_type='usdt',
                         symbol='DOGEUSDT',
                         order_type='MKT',
                         quantity=40,
                         price=None,
                         side='BUY',
                         direction='ENTRY',
                         leverage_size=1,
                         invest_amount=0.25 * 40,
                         margin_type='ISOLATED',
                         est_fill_cost=0,
                         signal_uid='test_uid',
                         paired=False,
                         retry=True,
                         retry_num=1)
    ord_evt.save()

    ord_evt.margin_type_confirmed = threading.Event()
    ord_evt.margin_type_confirmed.set()

    ord_evt.update()