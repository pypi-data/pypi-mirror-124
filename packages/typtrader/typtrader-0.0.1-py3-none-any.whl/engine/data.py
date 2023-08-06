import datetime
import threading
import numpy as np
import pandas as pd
from typing import Dict
from tradernetwork import Memory
from multiprocessing import shared_memory, Queue

from engine.events import SecondEvent
from api.data_client import DataClient
from engine.utils.distributed_queue import DistributedQueue
from params import (
    PROXY_HOST,
    DATA_PROXY_MARKET_PORT,
    STRATEGY_QUEUE_HOST,
    STRATEGY_PORTS,
    TMP_QUEUE_HOST,
    TMP_QUEUE_PORT,
)

SECOND_TABLE = {
    date: i for i, date in
    enumerate([d.strftime('%H%M%S') for d in pd.date_range('00:00:00', '23:59:59', freq='S')])
}

SYMBOL_TABLE = {
    'bybit.usdt.BTCUSDT': 0,
    'bybit.usdt.ETHUSDT': 1,
    'bybit.usdt.DOGEUSDT': 2,
    'bybit.usdt.ETCUSDT': 3,
    'bybit.coinm.BTCUSD': 4,
    'binance.spot.BTCUSDT': 5,
    'binance.spot.ETHUSDT': 6,
    'binance.spot.DOGEUSDT': 7,
    'binance.spot.ETCUSDT': 8,
    'binance.usdt.BTCUSDT': 9,
    'binance.usdt.ETHUSDT': 10,
    'binance.usdt.DOGEUSDT': 11,
    'binance.usdt.ETCUSDT': 12
}

FIELD_LIST = [
    'timestamp',
    'local_timestamp',
    'server_timestamp',
    'latency',
    'current_price',
    'open',
    'high',
    'low',
    'close',
    'volume',
    'tick_cnt',
    'buy_cnt',
    'buy_amt',
    'sell_cnt',
    'sell_amt'
]
FIELD_LIST.extend([f'sell_hoga{i}' for i in range(1, 26)])
FIELD_LIST.extend([f'sell_hoga{i}_stack' for i in range(1, 26)])
FIELD_LIST.extend([f'buy_hoga{i}' for i in range(1, 26)])
FIELD_LIST.extend([f'buy_hoga{i}_stack' for i in range(1, 26)])

FIELD_TABLE = {field: i for i, field in enumerate(FIELD_LIST)}

INDEX_TABLE = {
    'symbol': SYMBOL_TABLE,
    'field': FIELD_TABLE
}


class DataHandler:

    def __init__(self,
                 market_host: str = PROXY_HOST,
                 market_port: int = DATA_PROXY_MARKET_PORT,
                 strategy_host: str = STRATEGY_QUEUE_HOST,
                 strategy_ports: Dict[str, int] = STRATEGY_PORTS,
                 strategy_queues: Dict[str, Queue] = None,
                 tmp_host: str = TMP_QUEUE_HOST,
                 tmp_port: int = TMP_QUEUE_PORT,
                 tmp_queue: Queue = None,
                 debug: bool = False):
        """
        DataProxy로부터 데이터를 받아서 (DataClient 사용하여) shared memory에 데이터를 쌓고
        전략별로 소켓/큐로 SecondEvent를 보내주는 역할 수행

        데이터는 DataProxy로부터 직접받는 것이 아닌, DataClient를 사용하여 데이터를 받는다.

        :param market_host: DataProxy가 돌아가고 있는 서버 (보통은 로컬)
        :param market_port: DataProxy market_port와 동일
        :param strategy_host: Strategy 클래스와 DataHandler를 엮어주는 strategy_queue가 실행 중인 호스트
        :param strategy_ports: strategy_queue의 포트 (큐인 경우 불필요)
        :param strategy_queues: 큐를 만들어서 핸들러에 넣어줄 경우 소켓이 아닌 큐로 데이터를 주고 받는다
        :param tmp_host: shared memory 정보를 생성과 동시에 보내주기 위한 임시 큐가 실행중인 호스트 (소켓의 경우)
        :param tmp_port: tmp_queue의 포트 (큐인 경우 불필요)
        :param tmp_queue: 소켓이 아닌 큐로도 tmp_queue를 사용할 수 있다
        """

        self.debug = debug

        self.market_host = market_host
        self.market_port = market_port

        if strategy_queues is None:
            self.strategy_queues = {st: DistributedQueue(st_port, strategy_host)
                                    for st, st_port in strategy_ports.items()}
        else:
            self.strategy_queues = strategy_queues

        if tmp_queue is None:
            self.tmp_queue = DistributedQueue(tmp_port, tmp_host)
        else:
            self.tmp_queue = tmp_queue

        self.memory = Memory('mem', INDEX_TABLE)
        self.shared_mem_info = self.memory.mem_info
        self._init_shared_memory(self.shared_mem_info)

        if self.tmp_queue is not None:
            self.shared_mem_info['second_table'] = {}
            self.tmp_queue.put(self.shared_mem_info)

        self.last_event = datetime.datetime.now()

        self._emit_second_event()

    def _init_shared_memory(self, memory_info: dict):
        mem_name = memory_info['name']
        mem_shape = memory_info['shape']
        mem_dtype = memory_info['dtype']

        self.mem = shared_memory.SharedMemory(name=mem_name)
        self.mem_array = np.ndarray(shape=mem_shape, dtype=mem_dtype, buffer=self.mem.buf)

    def update_shared_memory(self, data: dict):
        symbol = f'{data["source"]}.{data["symbol"]}'
        symbol_idx = SYMBOL_TABLE[symbol]

        self.mem_array[symbol_idx, :] = list(data['data'].values())

        if self.debug:
            print(data['source'], data['symbol'])
            print(symbol_idx, self.mem_array[symbol_idx, 0:5])
            print('\n')

    def _emit_second_event(self):
        curr_timestamp = datetime.datetime.now()

        if (curr_timestamp - self.last_event).seconds >= 1:
            sec_evt = SecondEvent(local_timestamp=curr_timestamp.strftime('%Y%m%d%H%M%S%f')[:-3])
            for _, queue in self.strategy_queues.items():
                queue.put(sec_evt)
            self.last_event = curr_timestamp

        timer = threading.Timer(0.1, self._emit_second_event)
        timer.setDaemon(True)
        timer.start()

    def start_data_loop(self):
        print('Starting Data Handler')
        client = DataClient(market_host=self.market_host,
                            market_port=self.market_port,
                            debug=self.debug)
        client.stream_market_data(callback=self.update_shared_memory)


if __name__ == '__main__':
    dh = DataHandler(debug=False)
    dh.start_data_loop()