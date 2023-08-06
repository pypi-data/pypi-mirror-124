from engine.events.event import Event
from engine.events.fill_event import FillEvent
from engine.events.order_event import OrderEvent
from engine.events.signal_event import SignalEvent
from engine.events.pair_signal_event import PairSignalEvent
from engine.events.success_events import (
    TransferSuccessEvent,
    RepaySuccessEvent,
    LeverageSuccessEvent,
    MarginTypeSuccessEvent,
    OrderSuccessEvent,
    PairOrderSuccessEvent,
)


class RawDataEvent(Event):

    def __init__(self, raw_data: dict, **kwargs):
        self.type = 'RAW_DATA'
        self.raw_data = raw_data

    def message(self, module: str):
        pass


class HistoricalBarEvent(Event):

    def __init__(self,
                 local_timestamp: str,
                 freq: str,
                 **kwargs):

        self.type = 'HB'
        self.freq = freq
        self.local_timestamp = local_timestamp

    def message(self, module: str):
        pass


class SecondEvent(Event):

    def __init__(self, local_timestamp: str, **kwargs):
        self.type = 'SECOND'
        self.local_timestamp = local_timestamp

    def message(self, module: str):
        return f'[{module}] Second: {self.local_timestamp}'


class HourEvent(Event):

    def __init__(self, **kwargs):
        self.type = 'HOUR'

    def message(self, module: str):
        pass


class PairOrderEvent(Event):

    def __init__(self,
                 first_order: OrderEvent or dict,
                 second_order: OrderEvent or dict,
                 **kwargs):

        self.type = 'PAIR_ORDER'

        if isinstance(first_order, dict):
            self.first_order = OrderEvent(**first_order)
        else:
            self.first_order = first_order

        if isinstance(second_order, dict):
            self.second_order = OrderEvent(**second_order)
        else:
            self.second_order = second_order

    @property
    def __dict__(self):
        return {
            'type': self.type,
            'first_order': self.first_order.__dict__,
            'second_order': self.second_order.__dict__
        }

    def message(self, module: str):
        pass


class JangoEvent(Event):

    def __init__(self,
                 api_current_holdings: dict,
                 api_current_positions: dict,
                 **kwargs):

        self.type = 'JANGO'
        self.api_current_holdings = api_current_holdings
        self.api_current_positions = api_current_positions

    def message(self, module: str):
        pass


if __name__ == '__main__':
    he = HourEvent()
    print(he.__dict__)

    ord1 = OrderEvent('id1', 'bybit', 'usdt', 'BTCUSDT', 'MKT',
                      1, 100, 'BUY', 'ENTRY', 1, 'ISOLATED', 100, 'uid')
    ord2 = OrderEvent('id2', 'binance', 'usdt', 'BTCUSDT', 'MKT',
                      1, 100, 'BUY', 'ENTRY', 1, 'ISOLATED', 100, 'uid')

    pair_ord = PairOrderEvent(ord1, ord2)
    print(pair_ord.__dict__)

    new_pair_ord = PairOrderEvent(**pair_ord.__dict__)
    print(new_pair_ord.type)
    print(new_pair_ord.first_order)
    print(new_pair_ord.second_order)
