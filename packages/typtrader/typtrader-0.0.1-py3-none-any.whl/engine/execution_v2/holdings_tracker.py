import time
import redis
import threading
import numpy as np
from typing import List
import concurrent.futures
from flatten_dict import flatten, unflatten
from cointraderkr import CoinAPI, MetricCollector

from params import (
    API_KEYS,
    EXCHANGE_LIST,
    ASSET_LIST,
    SYMBOL_LIST,
    LOG_QUEUE_HOST,
    LOG_QUEUE_PORT,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PASSWORD,
    INFLUXDB_HOST,
    INFLUXDB_TOKEN,
    INFLUXDB_ORG,
    INFLUXDB_BUCKET,
)
from engine.utils.log import Logger


class HoldingsTracker:

    def __init__(self,
                 update_time: int = 30,
                 redis_host: str = REDIS_HOST,
                 redis_port: int = REDIS_PORT,
                 redis_password: str = REDIS_PASSWORD,
                 influxdb_host: str = INFLUXDB_HOST,
                 influxdb_token: str = INFLUXDB_TOKEN,
                 influxdb_org: str = INFLUXDB_ORG,
                 influxdb_bucket: str = INFLUXDB_BUCKET,
                 strategy_ls: List[str] = [],
                 debug: bool = False):

        self.debug = debug
        self.strategy_ls = strategy_ls
        self.update_time = update_time

        self.logger = Logger(debug=self.debug)

        self.api = {
            st: CoinAPI(binance_public_key=API_KEYS[st]['binance_public'],
                        binance_private_key=API_KEYS[st]['binance_private'],
                        bybit_public_key=API_KEYS[st]['bybit_public'],
                        bybit_private_key=API_KEYS[st]['bybit_private'])
            for st in self.strategy_ls
        }

        self.redis_conn = redis.StrictRedis(host=redis_host,
                                            port=redis_port,
                                            password=redis_password)

        self.mc = MetricCollector(host=influxdb_host,
                                  token=influxdb_token,
                                  org=influxdb_org,
                                  bucket=influxdb_bucket)

        self.current_positions = {}
        self.current_holdings = {}

        self.cur_hold_dict = {}
        self.curr_price_dict = self.symbol_padded_price()

    def symbol_padded_price(self):
        d = {}
        for e in EXCHANGE_LIST:
            d[e] = {}
            for a in ASSET_LIST:
                d[e][a] = {}
                for s in SYMBOL_LIST:
                    d[e][a][s] = np.nan
        return d

    def get_bybit_usdt_curr_price(self):
        price_dict = {}
        st = self.strategy_ls[0]
        for symbol in SYMBOL_LIST:
            res = self.api[st].bybit.client.LinearMarket.LinearMarket_trading(symbol=symbol).result()
            data = res[0]['result']
            curr_price = data[0]['price']
            price_dict[symbol] = curr_price
        return price_dict

    def get_binance_spot_curr_price(self):
        st = self.strategy_ls[0]
        res = self.api[st].binance.client.get_all_tickers()
        price_dict = {
            d['symbol']: float(d['price'])
            for d in res if d['symbol'] in SYMBOL_LIST
        }
        return price_dict

    def get_binance_usdt_curr_price(self):
        st = self.strategy_ls[0]
        res = self.api[st].binance.client._request_futures_api('get', 'ticker/price', False)
        price_dict = {
            d['symbol']: float(d['price'])
            for d in res if d['symbol'] in SYMBOL_LIST
        }
        return price_dict

    def update_curr_price(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future1 = executor.submit(self.get_bybit_usdt_curr_price)
            future2 = executor.submit(self.get_binance_usdt_curr_price)

            res1 = future1.result()
            res2 = future2.result()

        self.curr_price_dict['bybit']['usdt'] = res1
        self.curr_price_dict['binance']['usdt'] = res2

    def get_current_positions_from_redis(self, strategy_id: str):
        pos_key = f'position_{strategy_id}'
        res = self.redis_conn.hgetall(pos_key)
        res = {key.decode('utf-8'): float(val.decode('utf-8')) for key, val in res.items()}
        unflatten_res = unflatten(res, splitter='underscore')
        return unflatten_res

    def get_current_holdings_from_redis(self, strategy_id: str):
        hold_key = f'holdings_{strategy_id}'
        res = self.redis_conn.hgetall(hold_key)
        res = {key.decode('utf-8'): float(val.decode('utf-8')) for key, val in res.items()}
        unflatten_res = unflatten(res, splitter='underscore')
        return unflatten_res

    def update_holdings(self):
        self.current_positions = {st: self.get_current_positions_from_redis(st)
                                  for st in self.strategy_ls}
        self.current_holdings = {st: self.get_current_holdings_from_redis(st)
                                 for st in self.strategy_ls}

        self.update_curr_price()

        for e in EXCHANGE_LIST:
            if e == 'bybit':
                asset_list = ['usdt']
            elif e == 'binance':
                asset_list = ['spot', 'usdt']
            else:
                asset_list = []

            for st in self.strategy_ls:
                for a in asset_list:
                    self.current_holdings[st][e][a]['TotalValue'] = 0.0
                    if a == 'spot':
                        self.current_holdings[st][e][a]['TotalValue'] = self.current_holdings[st][e][a]['USDT']

                    long = [{'s': key, **val['long']} for key, val in self.current_positions[st][e][a].items()]
                    short = [{'s': key, **val['short']} for key, val in self.current_positions[st][e][a].items()]

                    symbol = [d['s'] for d in long]
                    curr_price = np.array([self.curr_price_dict[e][a][s] for s in symbol])

                    long_quantity = np.array([d['q'] for d in long])
                    long_mean_price = np.array([d['p'] for d in long])
                    long_leverage = np.array([d['leverage'] if d['leverage'] != 0 else 1 for d in long])
                    long_market_value = ((long_quantity / long_leverage) * long_mean_price) + (long_quantity * (curr_price - long_mean_price))

                    short_quantity = np.array([d['q'] for d in short])
                    short_mean_price = np.array([d['p'] for d in short])
                    short_leverage = np.array([d['leverage'] if d['leverage'] != 0 else 1 for d in short])
                    short_market_value = ((short_quantity / short_leverage) * short_mean_price) + (short_quantity * (short_mean_price - curr_price))

                    market_value = long_market_value + short_market_value
                    mask = np.isnan(market_value)
                    market_value = np.where(~mask, market_value, 0)

                    for i in range(len(symbol)):
                        self.current_holdings[st][e][a][symbol[i]] = market_value[i]

                    prev_value = float(self.current_holdings[st][e][a]['TotalValue'])
                    self.current_holdings[st][e][a]['TotalValue'] = prev_value + sum(market_value)

        self.update_current_holdings_to_redis()
        self.send_current_holdings_to_influxdb()

    def update_current_holdings_to_redis(self):
        s = time.time()
        for st in self.strategy_ls:
            hold_key = f'holdings_{st}'
            self.redis_conn.delete(hold_key)  # 업데이트전 전체 삭제, 과거 잔재 없에기
            flatten_pos = flatten(self.current_holdings[st], reducer='underscore')
            pipeline = self.redis_conn.pipeline()
            for k, v in flatten_pos.items():
                pipeline.hset(hold_key, k, v)
            pipeline.execute()
        self.logger.info(f'[HoldingsTracker] Updated all Current Holdings to Redis took {time.time() - s} sec.')

    def send_current_holdings_to_influxdb(self):
        for st in self.strategy_ls:
            data = {
                'binance_spot': float(self.current_holdings[st]['binance']['spot']['TotalValue']),
                'binance_margin': float(self.current_holdings[st]['binance']['margin']['TotalValue']),
                'binance_usdt': float(self.current_holdings[st]['binance']['usdt']['TotalValue']),
                'bybit_spot': float(self.current_holdings[st]['bybit']['spot']['USDT']),
                'bybit_usdt': float(self.current_holdings[st]['bybit']['usdt']['TotalValue'])
            }
            data['binance_total'] = data['binance_spot'] + data['binance_margin'] + data['binance_usdt']
            data['bybit_total'] = data['bybit_spot'] + data['bybit_usdt']
            data['total'] = data['binance_total'] + data['bybit_total']
            points = [
                {'measurement': 'holdings', 'strategy': st, 'field': key, 'value': val}
                for key, val in data.items()
            ]
            self.mc.send_metrics(points)

    def start_holdings_tracker_loop(self):
        self.logger.info('[HoldingsTracker] Starting Holdings Tracker')
        while True:
            t = threading.Thread(target=self.update_holdings)
            t.start()
            time.sleep(self.update_time)


if __name__ == '__main__':
    ht = HoldingsTracker(strategy_ls=['example'], debug=True)
    # ht.update_holdings()
    ht.start_holdings_tracker_loop()

    # while True:
    #     time.sleep(5)
    #     h = ht.get_current_holdings_from_redis('example')
    #     print('Price: ', ht.curr_price_dict)
    #     print(h['bybit']['usdt'])