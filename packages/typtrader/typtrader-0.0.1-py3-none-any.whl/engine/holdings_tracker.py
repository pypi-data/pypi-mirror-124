import os
import csv
import time
import redis
import datetime
import traceback
import threading
import numpy as np
from multiprocessing import shared_memory
from flatten_dict import flatten, unflatten

from engine_v2.bar import Bar
from engine_v2.log import Logger
from engine.utils.log import CoinTelegram
from operation.min_trade_amount import get_min_trade_amount

from dask.distributed import Client
from engine.utils.log import MetricCollector


EXCHANGE_LIST = [
    'binance',
    # 'bybit' # 다시 풀어주기
]

ASSET_LIST = [
    'usdt',
    'margin',
    'spot'
]

SYMBOL_LIST = [
    'BTCUSDT',
    'ETHUSDT',
    'DOGEUSDT',
    'ETCUSDT',
]

MIN_TRADE_AMOUNT = get_min_trade_amount()


def symbol_update_process(cur_price, current_positions, current_holdings, st, exchange, a, s):
    cur_long_quantity = float(current_positions[st][exchange][a][s]['long']['q'])
    cur_long_mean_price = float(current_positions[st][exchange][a][s]['long']['p'])
    cur_short_quantity = float(current_positions[st][exchange][a][s]['short']['q'])
    cur_short_mean_price = float(current_positions[st][exchange][a][s]['short']['p'])

    if np.isnan(cur_price):
        market_value = float(current_holdings[st][exchange][a][s]) # 999
    else:
        long_lev, short_lev = 1, 1
        long_market_value, short_market_value = 0, 0

        if cur_long_quantity != 0:
            long_lev = float(current_positions[st][exchange][a][s]['long']['leverage'])
            long_lev = 1 if long_lev == 0 else long_lev
            long_market_value = (cur_long_quantity / long_lev) * cur_long_mean_price + cur_long_quantity * (
                        cur_price - cur_long_mean_price)

        if cur_short_quantity != 0:
            short_lev = float(current_positions[st][exchange][a][s]['short']['leverage'])
            short_lev = 1 if short_lev == 0 else short_lev
            short_market_value = (cur_short_quantity / short_lev) * cur_short_mean_price + cur_short_quantity * (
                        cur_short_mean_price - cur_price)

        market_value = long_market_value + short_market_value

        # if s == "LINKUSDT" and a == "margin":
        #     print(f"long_market_value: {long_market_value} short_market_value: {short_market_value} "
        #           f"cur_long_mean_price: {cur_long_mean_price} cur_short_mean_price: {cur_short_mean_price}"
        #           f"market_value: {market_value} cur_price: {cur_price}")

    res = (st, exchange, a, s, market_value)

    return res


class Holdings_Tracker:
    def __init__(self,
                 sec_mem_name=None,
                 sec_mem_shape=None,
                 sec_mem_dtype=None,
                 second_table=None,
                 symbol_table=None,
                 field_table=None,
                 port_cls=None,
                 bar_cls=None,
                 log_queue=None,
                 backtest: bool = False):

        self.logger = Logger(log_queue)
        self.telebot = CoinTelegram()

        self.backtest = backtest

        if backtest:
            self.portfolio = port_cls
            self.bar = bar_cls

        self.cnt = 0
        self.today_str = datetime.datetime.now().strftime("%Y-%m-%d")

        self.dask_conn = Client(processes=True)

        if not backtest:
            self.redis_conn = redis.StrictRedis(host=os.getenv('REDIS_HOST'),
                                                port=os.getenv('REDIS_PORT'),
                                                password=os.getenv('REDIS_PW'),
                                                charset="utf-8",
                                                decode_responses=True,
                                                )

        ######### Strategy 와 곂치는 SHM 설정, 필요한지 검토 필요 ##########
        if not backtest:
            self.bar = Bar()
            self.sec_mem_shape = sec_mem_shape
            self.sec_mem = shared_memory.SharedMemory(name=sec_mem_name)
            self.sec_mem_array = np.ndarray(shape=sec_mem_shape, dtype=sec_mem_dtype,
                                            buffer=self.sec_mem.buf)

            self.bar.second_table = second_table
            self.bar.symbol_table = symbol_table
            self.bar.field_table = field_table
            self.bar.sec_mem_array = self.sec_mem_array

            self.mc = MetricCollector()
        ###############################################################

        self.strategy_ls = ['coin_arbit']

        # Positions만 있으면 Holdings를 구할수 있게 구현해야한다.
        self.current_positions = {}
        self.current_holdings = {}

        self.cur_hold_dict = {}
        self.symbol_padded_price_dict = self.symbol_padded_price()

    def symbol_padded_price(self):
        d = {}
        for e in EXCHANGE_LIST:
            d[e] = {}
            for a in ['spot', 'usdt' ,'margin']:
                d[e][a] = {}
                for s in SYMBOL_LIST:
                    d[e][a][s] = np.nan
        return d

    # get Current Position from Redis
    def get_current_positions_from_redis(self, strategy_id):
        if self.backtest:
            unflatten_res = self.portfolio.current_positions[strategy_id]
        else:
            pos_key = f'position_{strategy_id}'
            res = self.redis_conn.hgetall(pos_key)
            # unflatten_res = unflatten(res, splitter=make_splitter(delimiter='_'))
            unflatten_res = unflatten(res, splitter='underscore')
        return unflatten_res

    def get_current_holdings_from_redis(self, strategy_id):
        if self.backtest:
            unflatten_res = self.portfolio.current_holdings[strategy_id]
        else:
            hold_key = f'holdings_{strategy_id}'
            res = self.redis_conn.hgetall(hold_key)
            # unflatten_res = unflatten(res, splitter=make_splitter(delimiter='_'))
            unflatten_res = unflatten(res, splitter='underscore')
        return unflatten_res

    def update_cur_holdings_to_redis(self):
        if self.backtest:
            return

        s = time.time()
        # print("start redis")
        for st in self.strategy_ls:
            hold_key = f'holdings_{st}'
            # print("delete redis")
            self.redis_conn.delete(hold_key) # 업데이트전 전체 삭제, 과거 잔재 없에기

            flatten_pos = flatten(self.current_holdings[st], reducer='underscore')
            # Pipeline need for bulk hset of Position Table!
            pipeline = self.redis_conn.pipeline()
            # print("put redis")
            for k, v in flatten_pos.items():
                # print(f"hset {k}")
                pipeline.hset(hold_key, k, v)
            pipeline.execute()

        if self.cnt % 100 == 1:
            self.logger.debug(f"Update all Cur_Holdings to Redis took {time.time() - s} sec. @ HT")

    def symbol_update(self, st, exchange, a, s):
        # 임시방편 ToDo 시형이형한테 padding 처리 여부 물어보기
        cur_price = self.bar.get_latest_bar_value(exchange, a, s, 'current_price')
        # cur_price = self.bar.get_latest_bar(exchange, 'usdt', s, 'dict')['current_price']

        # print(exchange, a, s, cur_price)
        cur_long_quantity = float(self.current_positions[st][exchange][a][s]['long']['q'])
        cur_long_mean_price = float(self.current_positions[st][exchange][a][s]['long']['p'])
        cur_short_quantity = float(self.current_positions[st][exchange][a][s]['short']['q'])
        cur_short_mean_price = float(self.current_positions[st][exchange][a][s]['short']['p'])

        if np.isnan(cur_price):
            market_value = 999 # float(self.current_holdings[st][exchange][a][s]) # cur_price 중간에 끊기는거 인식하기 위해 9999 입력
        else:
            long_lev, short_lev = 1, 1
            long_market_value, short_market_value = 0, 0

            if cur_long_quantity != 0:
                long_lev = float(self.current_positions[st][exchange][a][s]['long']['leverage'])
                long_lev = 1 if long_lev == 0 else long_lev
                long_market_value = (cur_long_quantity / long_lev) * cur_long_mean_price + cur_long_quantity * (cur_price - cur_long_mean_price)
                # TODO :: 여기서 부터 다시 시작하기.
                # print(f"{cur_long_quantity} {cur_long_mean_price} {}")

            if cur_short_quantity != 0:
                short_lev = float(self.current_positions[st][exchange][a][s]['short']['leverage'])
                short_lev = 1 if short_lev == 0 else short_lev
                short_market_value = (cur_short_quantity / short_lev) * cur_short_mean_price + cur_short_quantity * (cur_short_mean_price - cur_price)
                # short_market_value = cur_short_quantity * cur_short_mean_price * 2 - cur_short_quantity * cur_price

            # if cur_long_quantity == 0 or cur_short_quantity == 0:
            #     print(exchange, a, s)

            market_value = long_market_value + short_market_value

            # if s == "LINKUSDT" and a == "margin":
            #     print(f"{self.cnt} long_market_value: {long_market_value} short_market_value: {short_market_value} "
            #           f"cur_long_mean_price: {cur_long_mean_price} cur_short_mean_price: {cur_short_mean_price}"
            #           f"market_value: {market_value} cur_price: {cur_price}")

        # pprint(self.current_holdings)

        self.current_holdings[st][exchange][a][s] = market_value

        float_total_value = float(self.current_holdings[st][exchange][a]['TotalValue'])
        self.current_holdings[st][exchange][a]['TotalValue'] = float_total_value + market_value

    def holdings_update(self, st, exchange):
        task_res_ls = []

        if exchange == "bybit":
            ASSET_LIST = ['usdt']
        elif exchange == 'binance':
            if self.backtest:
                ASSET_LIST = ['usdt']
            else:
                ASSET_LIST = ['spot', 'usdt', 'margin']
        else:
            ASSET_LIST = None

        for a in ASSET_LIST:
            self.current_holdings[st][exchange][a]['TotalValue'] = 0.0
            if a == "spot":
                self.current_holdings[st][exchange][a]['TotalValue'] = self.current_holdings[st][exchange][a]['USDT']
            task_cnt = 0
            tasks = []

            for s in SYMBOL_LIST:
                # Normal Loop
                self.symbol_update(st, exchange, a, s)

        #         # # Dask apply
        #         # 임시방편으로 padding 된 cur_price 사용하기
        #         # cur_price = self.bar.get_latest_bar(exchange, a, s, 'dict')['current_price']
        #         cur_price = self.bar.get_latest_bar_value(exchange, a, s, 'current_price')
        #
        #         if not np.isnan(cur_price):
        #             self.symbol_padded_price_dict[exchange][a][s] = cur_price
        #
        #         # if s == "LINKUSDT" and a == "spot":
        #         #     print(f'curprice:{cur_price},패딩한 가격:{self.symbol_padded_price_dict[exchange][a][s]}')
        #         tasks.append(self.dask_conn.submit(symbol_update_process,
        #                                            self.symbol_padded_price_dict[exchange][a][s],
        #                                            self.current_positions,
        #                                            self.current_holdings,
        #                                            st,
        #                                            exchange,
        #                                            a,
        #                                            s))
        #         task_cnt += 1
        #
        #         if task_cnt == 4 or SYMBOL_LIST[-1] == s:
        #             res = self.dask_conn.gather(tasks)
        #             task_res_ls += res
        #             # print(f'symbol update end : {a} {exchange} {s} @ HT')
        #             task_cnt = 0
        #             tasks = []
        #         else:
        #             res = None
        #
        # # print(task_res_ls)
        # # print(len(task_res_ls))
        # for res in task_res_ls:
        #     st, exchange, a, s, market_value = res
        #     self.current_holdings[st][exchange][a][s] = market_value
        #     float_total_value = float(self.current_holdings[st][exchange][a]['TotalValue'])
        #     self.current_holdings[st][exchange][a]['TotalValue'] = float_total_value + market_value

        # legacy
        # TODO : 펀딩피 관련 account msg를 연결해줘야 구현 가능함. 추후 펀딩피 자동화 원할시 구현하기
        # elif a == 'coinm':
        #     cur_price = self.bar.get_latest_bar(exchange, 'coinm', 'BTCUSD', 'dict')['current_price']
        #     cur_hold_dict['coinm']['BTCUSD'] = cur_price * \
        #                                           self.current_positions[st][exchange]['coinm']['BTCUSD'][
        #                                               'total_balance']
        #     cur_hold_dict['coinm']['BTCUSD_leftovers'] = cur_price * \
        #                                                     self.current_positions[st][exchange]['coinm'][
        #                                                         'BTCUSD']['leftovers']

        return self.current_holdings[st][exchange]

    def write_holdings_to_csv(self):
        total_hold_dict = {}
        for st in self.strategy_ls:
            if self.backtest:
                total_hold_dict[st] = {'datetime': self.bar.curr_time}
            else:
                total_hold_dict[st] = {'datetime': datetime.datetime.now()}
            # pprint(self.current_holdings)
            total_hold_dict[st].update(self.current_holdings[st])
            for e in EXCHANGE_LIST:
                s = time.time()
                total_hold_dict[st][e] = self.holdings_update(st, e)
                # print(f"holding update {e} :{time.time() - s} sec")

            # Write Csv
            flatten_hold_dict = flatten(total_hold_dict[st], reducer='underscore')
            # pprint(flatten_hold_dict)
            if self.backtest:
                file_name = "../log/backtest/" + "bt_" + st + "_" + self.today_str + "_all_holdings.csv"
            else:
                file_name = "./log/all_holdings/" + st + "_" + self.today_str + "_all_holdings.csv"
            file_exists = os.path.isfile(file_name)
            with open(file_name, 'a', newline='') as f:
                fieldnames = list(flatten_hold_dict.keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(flatten_hold_dict)

            flatten_pos_dict = flatten(self.current_positions['coin_arbit'], reducer='underscore')
            # pprint(flatten_pos_dict)
            if self.backtest:
                file_name = "../log/backtest/" + "bt_" + st + "_" + self.today_str + "_all_positions.csv"
            else:
                file_name = "./log/all_holdings/" + st + "_" + self.today_str + "_all_positions.csv"
            file_exists = os.path.isfile(file_name)
            with open(file_name, 'a', newline='') as f:
                fieldnames = list(flatten_pos_dict.keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(flatten_pos_dict)

    def holdings_to_influxdb(self):
        if self.backtest:
            return

        for st in self.strategy_ls:
            self.mc.use_bucket('test-taehun-bucket')
            total_value = float(self.current_holdings[st]['binance']['spot']['USDT'])+\
                          float(self.current_holdings[st]['binance']['margin']['TotalValue'])+\
                          float(self.current_holdings[st]['binance']['usdt']['TotalValue'])+\
                          float(self.current_holdings[st]['bybit']['spot']['USDT'])+\
                          float(self.current_holdings[st]['bybit']['usdt']['TotalValue'])

            points = [
                {'measurement': 'coin', 'strategy': st, 'field': 'chart1_total_USDT_value','value': round(total_value)},
                {'measurement': 'coin', 'strategy': st, 'field': 'chart2_binance_spot_USDT_ratio', 'value': round(float(self.current_holdings[st]['binance']['spot']['USDT'])/total_value,3)},
                {'measurement': 'coin', 'strategy': st, 'field': 'chart2_binance_margin_TotalValue_ratio', 'value': round(float(self.current_holdings[st]['binance']['margin']['TotalValue'])/total_value,3)},
                {'measurement': 'coin', 'strategy': st, 'field': 'chart2_binance_usdt_TotalValue_ratio', 'value': round(float(self.current_holdings[st]['binance']['usdt']['TotalValue'])/total_value,3)},
                {'measurement': 'coin', 'strategy': st, 'field': 'chart2_bybit_spot_USDT_ratio', 'value': round(float(self.current_holdings[st]['bybit']['spot']['USDT'])/total_value,3)},
                {'measurement': 'coin', 'strategy': st, 'field': 'chart2_bybit_usdt_TotalValue_ratio', 'value': round(float(self.current_holdings[st]['bybit']['usdt']['TotalValue'])/total_value,3)}
            ]

            self.mc.send_metrics(points)

    def holdings_thread(self):
        try:
            # 1. Redis Position 조회(매 10초 마다)
            s = time.time()
            self.current_positions = {st: self.get_current_positions_from_redis(st) for st in self.strategy_ls}
            self.current_holdings = {st: self.get_current_holdings_from_redis(st) for st in self.strategy_ls}
            # pprint(self.current_positions)
            # pprint(self.current_holdings)

            # 2. 조회한 Position으로 Update Holdings
            self.write_holdings_to_csv()
            e2 = time.time()

            # 3. Update한 holdings 정보를 Redis로 업데이트
            self.update_cur_holdings_to_redis()

            # 4. Update한 holdings 정보를 influxdb로 업데이트
            self.holdings_to_influxdb()

            e = time.time()
            self.cnt += 1
            # print(self.cnt)

            if self.cnt % 100 == 1:
                self.logger.info(f"Holdings Tracker Running Successfully: {e - s} sec. @ HT")
                # self.logger.info(f"Writing Csv Running Successfully: {e2 - s} sec. @ HT")
                self.cnt = 1
        except:
            traceback.print_exc()
            self.logger.error('!!!! error !!!! holdings tracker sleep for 5 sec @ HT')

    def start_holdings_tracker_loop(self):
        self.logger.debug('starting holdings tracker @ HT')
        while True:
            # TODO 프로그램 시작후 초기화된 position 및 holdings 정보를 먼저 받는게 중요
            thread = threading.Timer(5, self.holdings_thread)
            thread.start()
            time.sleep(5) # 필요


if __name__ == "__main__":
    cls = Holdings_Tracker(test_mode=False)
    # a = cls.get_current_positions_from_redis('coin_arbit')
    # pprint(dict(a))

    cls.start_holdings_tracker_loop()

    # h = cls.current_holdings
    # pprint(h)
