import os
import hashlib
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
application = get_wsgi_application()

from db.models import PairSignal
from engine.events.event import Event


class PairSignalEvent(Event):

    def __init__(self,
                 strategy_id: str,
                 long_info: str,
                 short_info: str,
                 signal_type: str,
                 long_cur_price: int or float,
                 short_cur_price: int or float,
                 order_type: str,

                 log_time: str = None,
                 signal_uid: str = None,
                 **kwargs):

        self.type = 'PAIR_SIGNAL'
        self.strategy_id = strategy_id
        self.long_info = long_info
        self.short_info = short_info
        self.signal_type = signal_type.upper()  # ENTRY, EXIT
        self.long_cur_price = long_cur_price
        self.short_cur_price = short_cur_price
        self.order_type = order_type.upper()  # MKT, LMT

        self.log_time = self._time() if log_time is None else log_time
        self.signal_uid = self._make_unique_id() if signal_uid is None else signal_uid

    def _make_unique_id(self):
        string = f'{self.strategy_id}_{self.long_info}_{self.short_info}_{self.log_time}_' \
                 f'{self.signal_type}_{self.order_type}'
        encoded_str = string.encode('utf-8')
        sha_string = hashlib.sha1(encoded_str).hexdigest()
        return sha_string

    def message(self, module: str):
        return f'[{module}]\n' \
               f'--- Type: {self.type} ---\n' \
               f'Long: {self.long_info}, Price: {self.long_cur_price}\n' \
               f'Short: {self.short_info}, Price: {self.long_cur_price}\n' \
               f'Signal: {self.signal_type}, Order: {self.order_type}\n' \
               f'UID: {self.signal_uid}\n' \
               f'Time: {self.log_time}'

    def save(self):
        PairSignal(**self.__dict__).stream_save()


if __name__ == '__main__':
    from engine.utils.distributed_queue import DistributedQueue

    TEST_PORT = 1111

    q = DistributedQueue(TEST_PORT)

    signal = PairSignalEvent(strategy_id='test',
                             long_info='binance_usdt_BTCUSDT',
                             short_info='bybit_usdt_BTCUDT',
                             signal_type='ENTRY',
                             long_cur_price=1000,
                             short_cur_price=1020,
                             order_type='MKT')

    evt_msg = signal.message(module='DEBUG')
    print(evt_msg)

    q.put(signal)

    signal_q = q.get()
    print(signal_q)
    print(signal_q.__dict__)

    signal.save()