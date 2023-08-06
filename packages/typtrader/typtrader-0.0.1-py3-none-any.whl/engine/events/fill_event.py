import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
application = get_wsgi_application()

from db.models import Fill
from engine.events.event import Event


class FillEvent(Event):

    def __init__(self,
                 strategy_id: str,
                 exchange: str,
                 asset_type: str,
                 symbol: str,
                 side: str,
                 direction: str,
                 filled_quantity: int or float,
                 order_quantity: int or float,
                 fill_cost: int or float,
                 est_fill_cost: int or float,
                 api_order_uid: str,
                 order_uid: str = None,
                 signal_uid: str = None,
                 accno: str = None,
                 log_time: str = None,
                 commission: int or float = None,
                 **kwargs):

        self.type = 'FILL'
        self.strategy_id = strategy_id               # Exec에서 Order와 Matching 해줌
        self.exchange = exchange                     # binance, bybit
        self.asset_type = asset_type                 # usdt, coinm, spot, margin
        self.symbol = symbol
        self.side = side                             # BUY, SELL
        self.direction = direction                   # ENTRY, EXIT
        self.filled_quantity = abs(filled_quantity)  # 체결 수량은 무조건 양수로 만들기. (side로 구분)
        self.order_quantity = order_quantity
        self.fill_cost = fill_cost
        self.est_fill_cost = est_fill_cost
        self.api_order_uid = api_order_uid
        self.matcher = f'{self.exchange}_{self.asset_type}_{self.symbol}_{self.side}_{str(float(self.order_quantity))}'

        self.order_uid = None if order_uid is None else order_uid
        self.signal_uid = None if signal_uid is None else signal_uid

        self.accno = None if accno is None else accno  # TODO :: Not used yet
        self.log_time = self._time() if log_time is None else log_time
        self.commission = self.calc_commission() if commission is None else commission

    def calc_commission(self):
        if self.api_order_uid == 'backtest':
            fill_cost = self.est_fill_cost
        else:
            fill_cost = self.fill_cost

        transaction_cost = None
        if fill_cost is not None:
            if self.exchange == 'binance':
                transaction_cost = 0.001 * fill_cost
            elif self.exchange == 'bybit':
                transaction_cost = 0.00075 * fill_cost
            else:
                raise Exception('Unknown Exchange! @ FillEvent')
        return transaction_cost

    def message(self, module: str):
        return f'[{module}]\n' \
               f'[{self.exchange.upper()} {self.asset_type.upper()}] {self.symbol.upper()} {self.side.upper()} ORDER FILLED\n' \
               f'- Order Quantity: {self.order_quantity}\n' \
               f'- Filled Quantity: {self.filled_quantity}\n' \
               f'- Order ID: {self.api_order_uid}'

    def save(self):
        return Fill(**self.__dict__).stream_save()


if __name__ == '__main__':
    from engine.utils.distributed_queue import DistributedQueue

    q = DistributedQueue(9999)

    evt = FillEvent(strategy_id='test',
                    exchange='binance',
                    asset_type='usdt',
                    symbol='DOGEUSDT',
                    filled_quantity=1,
                    order_quantity=10,
                    side='BUY',
                    fill_cost=0,
                    est_fill_cost=0,
                    api_order_uid='123123')

    q.put(evt)

    evt_q = q.get()
    print(evt_q.message('test'))