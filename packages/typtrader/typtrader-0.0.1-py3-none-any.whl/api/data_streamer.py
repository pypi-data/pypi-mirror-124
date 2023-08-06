from typing import List
from multiprocessing import Process
from tradernetwork import PullSocket, ProxySocket, PubSocket
from traderstreamer import (
    BinanceMarketStreamerService,
    BybitMarketStreamerService,
    BinanceAccountStreamerService,
    BybitAccountStreamerService,
    BinanceSecondBarService,
    BybitSecondBarService,
)

from params import API_KEYS

MONITOR_COINS = ['BTCUSDT', 'ETHUSDT', 'DOGEUSDT', 'ETCUSDT']


def run_binance_market_streamer_svc_1(port: int):
    svc = BinanceMarketStreamerService('binance-market-streamer-svc-1',
                                       'binance_market_streamer_1',
                                       options={'auto_restart': True},
                                       name='binance_market_streamer',
                                       market='spot',
                                       monitor_coins=MONITOR_COINS,
                                       pub_port=port,
                                       verbose=False)
    svc.start()


def run_binance_market_streamer_svc_2(port: int):
    svc = BinanceMarketStreamerService('binance-market-streamer-svc-2',
                                       'binance_market_streamer_2',
                                       options={'auto_restart': True},
                                       name='binance_market_streamer',
                                       market='usdt',
                                       monitor_coins=MONITOR_COINS,
                                       pub_port=port,
                                       verbose=False)
    svc.start()


def run_binance_account_streamer_svc_1(port: int):
    svc = BinanceAccountStreamerService('binance-account-streamer-svc-1',
                                        'binance_account_streamer_1',
                                        options={'auto_restart': True},
                                        name='binance_account_streamer',
                                        market='margin',
                                        push_host='localhost',
                                        push_port=port,
                                        public_key=API_KEYS['example']['binance_public'],
                                        private_key=API_KEYS['example']['binance_private'],
                                        monitor_coins=MONITOR_COINS,
                                        verbose=False)
    svc.start()


def run_binance_account_streamer_svc_2(port: int):
    svc = BinanceAccountStreamerService('binance-account-streamer-svc-2',
                                        'binance_account_streamer_2',
                                        options={'auto_restart': True},
                                        name='binance_account_streamer',
                                        market='usdt',
                                        push_host='localhost',
                                        push_port=port,
                                        public_key=API_KEYS['example']['binance_public'],
                                        private_key=API_KEYS['example']['binance_private'],
                                        monitor_coins=MONITOR_COINS,
                                        verbose=False)
    svc.start()


def run_bybit_market_streamer_svc(port: int):
    svc = BybitMarketStreamerService('bybit-market-streamer-svc',
                                     'bybit_market_streamer',
                                     options={'auto_restart': True},
                                     name='bybit_market_streamer',
                                     market='usdt',
                                     monitor_coins=MONITOR_COINS,
                                     pub_port=port,
                                     verbose=False)
    svc.start()


def run_bybit_account_streamer_svc(port: int):
    svc = BybitAccountStreamerService('bybit-account-streamer-svc',
                                      'bybit_account_streamer',
                                      options={'auto_restart': True},
                                      name='bybit_account_streamer',
                                      market='usdt',
                                      push_host='localhost',
                                      push_port=port,
                                      public_key=API_KEYS['example']['bybit_public'],
                                      private_key=API_KEYS['example']['bybit_private'],
                                      verbose=False)
    svc.start()


def run_bybit_sec_svc(mkt_ports: List[int], port: int):
    monitor_coins = [f'usdt.{symbol}' for symbol in MONITOR_COINS]
    svc = BybitSecondBarService('bybit-second-bar-svc',
                                'bybit_second_bar',
                                options={'auto_restart': True},
                                push_host='localhost',
                                push_port=port,
                                sub_host='localhost',
                                sub_ports={f'bybit_{i}': port for i, port in enumerate(mkt_ports)},
                                monitor_coins=monitor_coins,
                                use_timestamp='local_timestamp',
                                verbose=False)
    svc.start()


def run_binance_sec_svc(mkt_ports: List[int], port: int):
    monitor_coins = [f'spot.{symbol}' for symbol in MONITOR_COINS] + [f'usdt.{symbol}' for symbol in MONITOR_COINS]
    svc = BinanceSecondBarService('binance-second-bar-svc',
                                  'binance_second_bar',
                                  options={'auto_restart': True},
                                  push_host='localhost',
                                  push_port=port,
                                  sub_host='localhost',
                                  sub_ports={f'binance_{i}': port for i, port in enumerate(mkt_ports)},
                                  monitor_coins=monitor_coins,
                                  use_timestamp='local_timestamp',
                                  verbose=False)
    svc.start()


class DataStreamer:

    pub_socket = None

    def __init__(self, ports: List[int] = list(range(1000, 1008))):
        self.bi_mkt_1_port = ports[0]
        self.bi_mkt_2_port = ports[1]
        self.by_mkt_port = ports[2]

        self.bi_acc_1_port = ports[3]
        self.bi_acc_2_port = ports[4]
        self.by_acc_port = ports[5]

        self.bi_mkt_ports = [self.bi_mkt_1_port, self.bi_mkt_2_port]
        self.by_mkt_ports = [self.by_mkt_port]

        self.bi_sec_port = ports[6]
        self.by_sec_port = ports[7]

    def stream_market_data(self):
        mp1 = Process(target=run_binance_market_streamer_svc_1, args=(self.bi_mkt_1_port,))
        mp1.start()

        mp2 = Process(target=run_binance_market_streamer_svc_2, args=(self.bi_mkt_2_port,))
        mp2.start()

        mp3 = Process(target=run_bybit_market_streamer_svc, args=(self.by_mkt_port,))
        mp3.start()

    def stream_account_data(self):
        ap1 = Process(target=run_binance_account_streamer_svc_1, args=(self.bi_acc_1_port,))
        ap1.start()

        ap2 = Process(target=run_binance_account_streamer_svc_2, args=(self.bi_acc_2_port,))
        ap2.start()

        ap3 = Process(target=run_bybit_account_streamer_svc, args=(self.by_acc_port,))
        ap3.start()

    def start_second_service(self):
        sp1 = Process(target=run_binance_sec_svc, args=(self.bi_mkt_ports, self.bi_sec_port))
        sp1.start()

        sp2 = Process(target=run_bybit_sec_svc, args=(self.by_mkt_ports, self.by_sec_port))
        sp2.start()

    def start_data_publisher(self, port: int):
        self.pub_socket = PubSocket(port)

        proxy = ProxySocket({
            'binance_sec_svc': PullSocket(self.bi_sec_port),
            'bybit_sec_svc': PullSocket(self.by_sec_port),
            'binance_account_svc_1': PullSocket(self.bi_acc_1_port),
            'binance_account_svc_2': PullSocket(self.bi_acc_2_port),
            'bybit_account_svc': PullSocket(self.by_acc_port)
        })
        proxy.callback = self.publish_data
        proxy.start_proxy_server_loop()

    def publish_data(self, socket_name: str, data: dict):
        self.pub_socket.publish({'source': socket_name, 'data': data})


if __name__ == '__main__':
    import time

    ports = list(range(30000, 30008))
    pub_port = 30010

    streamer = DataStreamer(ports)

    streamer.stream_market_data()
    time.sleep(5)

    streamer.stream_account_data()
    time.sleep(5)

    streamer.start_second_service()

    streamer.start_data_publisher(pub_port)