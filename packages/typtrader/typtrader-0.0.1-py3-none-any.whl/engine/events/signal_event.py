import os
import hashlib
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
application = get_wsgi_application()

from db.models import Signal
from engine.events.event import Event


class SignalEvent(Event):

    def __init__(self,
                 strategy_id: str,
                 exchange: str,
                 asset_type: str,
                 symbol: str,
                 signal_type: str,
                 signal_price: int or float,
                 order_type: str,

                 log_time: str = None,
                 signal_uid: str = None,
                 **kwargs):

        self.type = 'SIGNAL'
        self.strategy_id = strategy_id
        self.exchange = exchange.lower()
        self.asset_type = asset_type.lower()
        self.symbol = symbol.upper()
        self.signal_type = signal_type.upper()  # ENTRY, EXIT
        self.signal_price = signal_price
        self.order_type = order_type.upper()  # MKT, LMT

        self.log_time = self._time() if log_time is None else log_time
        self.signal_uid = self._make_unique_id() if signal_uid is None else signal_uid

    def _make_unique_id(self):
        string = f'{self.strategy_id}_{self.exchange}_{self.asset_type}_{self.symbol}_{self.log_time}_' \
                 f'{self.signal_type}_{self.order_type}'
        encoded_str = string.encode('utf-8')
        sha_string = hashlib.sha1(encoded_str).hexdigest()
        return sha_string

    def message(self, module: str):
        return f'[{module}]\n' \
               f'--- Type: {self.type} ---\n' \
               f'Strategy ID: {self.strategy_id}\n' \
               f'Exchange: {self.exchange}, Asset: {self.asset_type}, Symbol: {self.symbol}\n' \
               f'Signal: {self.signal_type}, Price: {self.signal_price}, Order: {self.order_type}\n' \
               f'UID: {self.signal_uid}\n' \
               f'Time: {self.log_time}'

    def save(self):
        Signal(**self.__dict__).stream_save()


if __name__ == '__main__':
    signal = SignalEvent(strategy_id='test',
                         exchange='binance',
                         asset_type='usdt',
                         symbol='BTCUSDT',
                         signal_type='ENTRY',
                         signal_price=100,
                         order_type='MKT')

    evt_msg = signal.message(module='DEBUG')
    print(evt_msg)

    signal.save()
