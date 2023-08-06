from multiprocessing import Queue

from engine.bar import Bar
from api.bar_deque import BarDeque
from engine.strategy import Strategy
from engine.events import (
    SignalEvent,
    OrderEvent,
    HourEvent,
    OrderSuccessEvent,
)
from engine.portfolio import Portfolio
from params import (
    STRATEGY_QUEUE_HOST,
    EXAMPLE_STRATEGY_QUEUE_PORT,
    EXECUTION_QUEUE_HOST,
    EXECUTION_QUEUE_PORT,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PASSWORD,
    PROXY_HOST,
    DATA_PROXY_BAR_PORT,
)


class ExampleStrategy(Strategy):

    def __init__(self,
                 strategy_host: str = STRATEGY_QUEUE_HOST,
                 strategy_port: int = EXAMPLE_STRATEGY_QUEUE_PORT,
                 strategy_queue: Queue = None,
                 execution_host: str = EXECUTION_QUEUE_HOST,
                 execution_port: int = EXECUTION_QUEUE_PORT,
                 execution_queue: Queue = None,
                 redis_host: str = REDIS_HOST,
                 redis_port: int = REDIS_PORT,
                 redis_password: str = REDIS_PASSWORD,
                 sec_mem_name: str = None,
                 sec_mem_shape: list or tuple = None,
                 sec_mem_dtype: str = None,
                 second_table: dict = {},
                 symbol_table: dict = {},
                 field_table: dict = {},
                 backtest: bool = False,
                 port_cls: Portfolio = None,
                 bar_cls: Bar = None,
                 debug: bool = False):

        super().__init__(strategy_host,
                         strategy_port,
                         strategy_queue,
                         execution_host,
                         execution_port,
                         execution_queue,
                         redis_host,
                         redis_port,
                         redis_password,
                         sec_mem_name,
                         sec_mem_shape,
                         sec_mem_dtype,
                         second_table,
                         symbol_table,
                         field_table,
                         backtest,
                         port_cls,
                         bar_cls,
                         debug)

        self.strategy_id = 'example'
        self.sent_order = False

        self.make_universe()

    def make_universe(self):
        self.bar = BarDeque(sub_host=PROXY_HOST,
                            sub_port=DATA_PROXY_BAR_PORT,
                            strategy_queue=self.strategy_queue,
                            exchange='bybit',
                            monitor_coins=['usdt.ETHUSDT', 'usdt.ETCUSDT', 'usdt.DOGEUSDT', 'usdt.BTCUSDT'],
                            interval='60m',
                            maxlen=200)

    def calc_signals(self, event: HourEvent):
        print(event)

        print(self.bar.df['usdt.BTCUSDT'])
        print(self.bar.df['usdt.ETHUSDT'])
        # bybit_price = self.get_latest_bar_value('bybit', 'usdt', 'DOGEUSDT', 'current_price')
        # binance_price = self.get_latest_bar_value('binance', 'usdt', 'DOGEUSDT', 'current_price')
        # print(f'Bybit: {bybit_price}, Binance: {binance_price}')
        #
        # # Signal
        # if not self.sent_order:
        #     sig_evt = SignalEvent(strategy_id=self.strategy_id,
        #                           symbol='DOGEUSDT',
        #                           exchange='bybit',
        #                           asset_type='usdt',
        #                           signal_type='ENTRY',
        #                           signal_price=bybit_price,
        #                           order_type='MKT')
        #     self.execution_queue.put(sig_evt)
        #
        #     # Order
        #     ord_evt = OrderEvent(strategy_id=self.strategy_id,
        #                          exchange='binance',
        #                          asset_type='usdt',
        #                          symbol='DOGEUSDT',
        #                          order_type='MKT',
        #                          quantity=50,
        #                          price=None,
        #                          side='BUY',
        #                          direction='ENTRY',
        #                          leverage_size=3,
        #                          invest_amount=bybit_price * 50,
        #                          margin_type='ISOLATED',
        #                          est_fill_cost=0,
        #                          signal_uid=sig_evt.signal_uid,
        #                          paired=False)
        #     self.execution_queue.put(ord_evt)
        #
        #     self.sent_order = True

    def handle_order_success_event(self, event: OrderSuccessEvent):
        print(event)


if __name__ == '__main__':
    # from params import TMP_QUEUE_HOST, TMP_QUEUE_PORT
    # from engine.utils.distributed_queue import DistributedQueue
    # from components import open_process, start_data_handler

    # open_process(start_data_handler)
    #
    # tmp_queue = DistributedQueue(TMP_QUEUE_PORT, TMP_QUEUE_HOST)
    #
    # shared_mem_info = tmp_queue.get()
    #
    # sec_mem_name = shared_mem_info['name']
    # sec_mem_shape = shared_mem_info['shape']
    # sec_mem_dtype = shared_mem_info['dtype']
    # second_table = shared_mem_info['second_table']
    # symbol_table = shared_mem_info['symbol_table']
    # field_table = shared_mem_info['field_table']
    #
    # strat = ExampleStrategy(sec_mem_name=sec_mem_name,
    #                         sec_mem_shape=sec_mem_shape,
    #                         sec_mem_dtype=sec_mem_dtype,
    #                         second_table=second_table,
    #                         symbol_table=symbol_table,
    #                         field_table=field_table)
    # strat.start_strategy_loop()

    strat = ExampleStrategy()
    strat.start_strategy_loop()