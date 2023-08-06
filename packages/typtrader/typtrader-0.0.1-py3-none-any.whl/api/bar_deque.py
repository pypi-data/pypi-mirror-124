import time
import datetime
import threading
import pandas as pd
from typing import List
from collections import deque
from tradernetwork import SubSocket, ProxySocket

from cointraderkr import BybitAPI
from engine.events import HourEvent
from engine.utils.distributed_queue import DistributedQueue
from params import (
    PROXY_HOST,
    DATA_PROXY_BAR_PORT,
)


def get_bybit_usdt_futures_data(symbol: str,
                                interval: str,
                                start_str: str = None,
                                maxlen: int = None):

    if start_str is None and maxlen is None:
        raise Exception('Request requires either start_str or maxlen')

    interval_int = int(interval.replace('m', ''))

    if interval_int not in [1, 60]:
        raise Exception('Data request can only take intervals of: 1m, 60m')

    if interval_int < 60:
        date_fmt = '%Y-%m-%d %H:%M:00'
        timedelta = pd.Timedelta(minutes=interval_int)
        if maxlen is not None:
            time_now = datetime.datetime.now()
            start_str = (time_now - pd.Timedelta(minutes=maxlen)).strftime(date_fmt)
    else:
        hour_cnt = interval_int / 60
        date_fmt = '%Y-%m-%d %H:00:00'
        timedelta = pd.Timedelta(hours=hour_cnt)
        if maxlen is not None:
            time_now = datetime.datetime.now()
            start_str = (time_now - pd.Timedelta(hours=maxlen)).strftime(date_fmt)

    api = BybitAPI()
    end_str = (datetime.datetime.now() - timedelta).strftime(date_fmt)
    done = False
    result = pd.DataFrame()

    cnt = 0

    while not done:
        data = api.get_usdt_futures_data(symbol, interval, start_str)
        data = data[['start_at', 'open', 'high', 'low', 'close', 'volume']]
        result = pd.concat([result, data], axis=0)
        if end_str in [d.strftime(date_fmt) for d in list(data['start_at'])]:
            done = True
        else:
            start_str = (data['start_at'].iloc[-1] + timedelta).strftime(date_fmt)
            cnt += 1
            if cnt == 10:
                # 1초에 10번 요청 보내도록 강제화
                time.sleep(1)
                cnt = 0
            else:
                time.sleep(0.1)

    if maxlen is None:
        result = result.reset_index(drop=True)
    else:
        result = result.iloc[-maxlen:].reset_index(drop=True)
    return result


class BarDeque:

    df = {}
    raw_data = {}
    data = {}
    received_dates = {}

    def __init__(self,
                 sub_host: str = PROXY_HOST,
                 sub_port: int = DATA_PROXY_BAR_PORT,
                 strategy_host: str = None,
                 strategy_port: int = None,
                 strategy_queue: DistributedQueue = None,
                 exchange: str = 'bybit',
                 monitor_coins: List[str] = ['usdt.ETHUSDT', 'usdt.ETCUSDT', 'usdt.DOGEUSDT', 'usdt.BTCUSDT'],
                 interval: str = '60m',
                 maxlen: int = 200):

        if maxlen % 200 != 0:
            raise Exception('maxlen can only be multiples of 200: i.e. 200, 400, 600, ... 1000, 2000')

        if strategy_queue is None:
            self.strategy_queue = DistributedQueue(strategy_port, strategy_host)
        else:
            self.strategy_queue = strategy_queue

        self.exchange = exchange
        self.monitor_coins = monitor_coins
        self.interval = interval
        self.maxlen = maxlen
        self.sockets = {
            'bybit_hr_streamer': SubSocket(sub_port, sub_host)
        }

        self.init_done = False
        self._init_make_data(lookback_window=maxlen)
        self._start_proxy()

    def _init_make_data(self, lookback_window: int):
        now_time = f'{datetime.datetime.now().strftime("%Y-%m-%d %H")}:00:00'
        start_time = datetime.datetime.now() - datetime.timedelta(hours=lookback_window)
        start_time = f'{start_time.strftime("%Y-%m-%d %H")}:00:00'

        date_range = pd.date_range(start_time, now_time, freq='1h')
        date_range = date_range[1:]

        for ticker_ in self.monitor_coins:
            data_f_temp = get_bybit_usdt_futures_data(ticker_.split('.')[1], '60m', maxlen=self.maxlen)
            data_f_temp['timestamp'] = date_range
            data_f_temp['timestamp'] = data_f_temp['timestamp'].apply(lambda d: d.strftime('%Y%m%d%H%M%S'))
            data_f_temp = data_f_temp[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
            data_f_temp = list(data_f_temp.T.to_dict().values())
            data_f_temp = [{'source': 'bybit', 'symbol': ticker_, 'data': d} for d in data_f_temp]
            for d in data_f_temp:
                self.callback('', d)
            print(f'Initialized data for {ticker_}')

        self.init_done = True

    def _start_proxy(self):
        self.proxy = ProxySocket(self.sockets)
        self.proxy.callback = self.callback

        t = threading.Thread(target=self.proxy.start_proxy_server_loop)
        t.start()

    def _format_df(self, df: pd.DataFrame):
        df.index = pd.to_datetime(df['timestamp'], format='%Y%m%d%H%M%S')
        df.drop('timestamp', axis=1, inplace=True)
        return df

    def _update_bar(self, symbol: str, data: dict):
        if symbol not in self.raw_data:
            self.raw_data[symbol] = deque([], maxlen=self.maxlen)

        self.raw_data[symbol].append(data['data'])
        self.df[symbol] = self._format_df(pd.DataFrame(self.raw_data[symbol]))

        if len(set([d[-1]['timestamp'] for _, d in self.raw_data.items()])) == 1:
            close_data = {}
            volume_data = {}
            for symbol, raw_data in self.raw_data.items():
                if 'timestamp' not in close_data:
                    close_data['timestamp'] = [d['timestamp'] for d in self.raw_data[symbol]]
                if 'timestamp' not in volume_data:
                    volume_data['timestamp'] = [d['timestamp'] for d in self.raw_data[symbol]]
                close_data[symbol] = [d['close'] for d in self.raw_data[symbol]]
                volume_data[symbol] = [d['volume'] for d in self.raw_data[symbol]]

            close_df = pd.DataFrame(close_data)
            volume_df = pd.DataFrame(volume_data)

            self.data['close'] = self._format_df(close_df)
            self.data['volume'] = self._format_df(volume_df)

            if self.strategy_queue is not None:
                if self.init_done:
                    self.strategy_queue.put(HourEvent())

    def callback(self, socket_name: str, data: dict):
        date_fmt = '%Y%m%d%H%M%S'
        data['data']['timestamp'] = (datetime.datetime.strptime(data['data']['timestamp'], date_fmt) - pd.Timedelta(hours=1)).strftime(date_fmt)
        symbol = data['symbol']
        timestamp = data['data']['timestamp']

        if symbol not in self.received_dates:
            self.received_dates[symbol] = deque([], maxlen=24)

        if timestamp not in self.received_dates[symbol]:
            self.received_dates[symbol].append(timestamp)
            self._update_bar(symbol, data)


if __name__ == '__main__':
    dq = BarDeque(strategy_port=1999, maxlen=400)

    time.sleep(3)

    print(dq.df['usdt.BTCUSDT'])
    print(dq.df['usdt.ETHUSDT'])
