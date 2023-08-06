import os
import redis
import traceback
import numpy as np
from dotenv import load_dotenv
from multiprocessing import shared_memory, Queue

from engine.bar import Bar
from engine.portfolio import Portfolio
from engine.utils.log import CoinTelegram, Logger
from engine.utils.distributed_queue import DistributedQueue
from engine.events import (
    SecondEvent,
    HourEvent,
    SignalEvent,
    PairSignalEvent,
    OrderSuccessEvent,
)

load_dotenv(override=True)

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_PASSWORD = os.getenv('REDIS_PW')


class Strategy:

    def __init__(self,
                 strategy_host: str = 'localhost',
                 strategy_port: int = 2000,
                 strategy_queue: Queue = None,
                 execution_host: str = 'localhost',
                 execution_port: int = 1004,
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

        self.debug = debug
        self.backtest = backtest

        if strategy_queue is None:
            self.strategy_queue = DistributedQueue(strategy_port, strategy_host)
            print(f'[Strategy] Created Strategy DistributedQueue at tcp://{strategy_host}:{strategy_port}')
        else:
            self.strategy_queue = strategy_queue

        if execution_queue is None:
            self.execution_queue = DistributedQueue(execution_port, execution_host)
            print(f'[Strategy] Created Execution DistributedQueue at tcp://{execution_host}:{execution_port}')
        else:
            self.execution_queue = execution_queue

        self.logger = Logger(debug=self.debug)
        self.telegram = CoinTelegram(debug=self.debug)

        if self.backtest:
            self.portfolio = port_cls
            self.bar = bar_cls
        else:
            self.bar = Bar()

            if sec_mem_shape is not None and \
                sec_mem_shape is not None and \
                    sec_mem_dtype is not None:
                self.bar.sec_mem = shared_memory.SharedMemory(name=sec_mem_name)
                self.bar.sec_mem_array = np.ndarray(shape=sec_mem_shape,
                                                    dtype=sec_mem_dtype,
                                                    buffer=self.bar.sec_mem.buf)

                self.bar.second_table = second_table
                self.bar.symbol_table = symbol_table
                self.bar.field_table = field_table
                print(f'[Strategy] Shared memory initialized: {sec_mem_name} {sec_mem_shape}')
            else:
                print(f'[Strategy] Shared memory initialization failed: missing sec_mem_shape / sec_mem_shape / sec_mem_dtype')

        # 전략을 실행시키려면 잔고 데이터가 가장 먼저 설정되어야 하기 때문에
        # 이를 강제화하기 위한 수단
        self.jango_updated = False
        self.port_updated = False

        if not self.backtest:
            self.redis_conn = redis.StrictRedis(host=redis_host,
                                                port=redis_port,
                                                password=redis_password)

    # Bar related functions and properties
    @property
    def sec_mem(self):
        return self.bar.sec_mem

    @property
    def sec_mem_array(self):
        return self.bar.sec_mem_array

    @property
    def second_table(self):
        return self.bar.second_table

    @property
    def symbol_table(self):
        return self.bar.symbol_table

    @property
    def field_table(self):
        return self.bar.field_table

    def get_latest_bar_value(self,
                             exchange: str,
                             asset_type: str,
                             symbol: str,
                             field: str):
        return self.bar.get_latest_bar_value(exchange=exchange,
                                             asset_type=asset_type,
                                             symbol=symbol,
                                             field=field)

    def redis_position_setter(self, strategy_id, exchange, asset_type, symbol, long_short, p_q_lev, value):
        if self.backtest:
            self.portfolio.current_positions[strategy_id][exchange][asset_type][symbol][long_short][p_q_lev] = value
        else:
            pos_key = f'position_{strategy_id}'
            pos_field = f'{exchange}_{asset_type}_{symbol}_{long_short}_{p_q_lev}'
            self.redis_conn.hset(pos_key, pos_field, value)

    def redis_holdings_setter(self, strategy_id, exchange, asset_type, symbol, value):
        if self.backtest:
            self.portfolio.current_holdings[strategy_id][exchange][asset_type][symbol] = value
        else:
            pos_key = f'holdings_{strategy_id}'
            pos_field = f'{exchange}_{asset_type}_{symbol}'
            self.redis_conn.hset(pos_key, pos_field, value)

    def send_signal(self,
                    strategy_id: str,
                    exchange: str,
                    asset_type: str,
                    symbol: str,
                    signal_type: str,
                    signal_price: int or float,
                    order_type: str):
        signal = SignalEvent(strategy_id=strategy_id,
                             exchange=exchange,
                             asset_type=asset_type,
                             symbol=symbol,
                             signal_type=signal_type,
                             signal_price=signal_price,
                             order_type=order_type)
        self.execution_queue.put(signal)

    def send_pair_signal(self,
                         strategy_id: str,
                         long_info: str,
                         short_info: str,
                         signal_type: str,
                         long_cur_price: int or float,
                         short_cur_price: int or float,
                         order_type: str):
        signal = PairSignalEvent(strategy_id=strategy_id,
                                 long_info=long_info,
                                 short_info=short_info,
                                 signal_type=signal_type,
                                 long_cur_price=long_cur_price,
                                 short_cur_price=short_cur_price,
                                 order_type=order_type)
        self.execution_queue.put(signal)

    def make_universe(self):
        raise NotImplementedError('[Strategy] make_universe 함수 미반영')

    def calc_signals(self, event: SecondEvent or HourEvent):
        raise NotImplementedError('[Strategy] calc_signals 함수 미반영')

    def handle_order_success_event(self, event: OrderSuccessEvent):
        raise NotImplementedError('[Strategy] handle_order_success_event 함수 미반영')

    def start_strategy_loop(self):
        """
        Portfolio 클래스의 이벤트 루프를 실행하여,
        DataHandler의 second Event, Strategy의 OrderEvent, (Execution의 FillEvent) 를 기다린다.
        Event가 도달하면 바로 처리하는 방식으로 작동한다.
        """
        while True:
            event = self.strategy_queue.get()
            try:
                if event.type == 'SECOND':
                    self.calc_signals(event)

                elif event.type == 'HOUR':
                    self.calc_signals(event)

                elif event.type == 'ORDER_SUCCESS':
                    self.handle_order_success_event(event)

                else:
                    self.logger.debug(f'[Strategy] Unknown Event type: {event.type}')
            except:
                self.logger.exception(traceback.format_exc())