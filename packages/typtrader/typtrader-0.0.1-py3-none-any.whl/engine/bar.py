import datetime
import pandas as pd
import numpy as np


class Bar:

    def __init__(self):
        self.sec_mem = None
        self.sec_mem_array = None
        self.second_table = None
        self.symbol_table = None
        self.field_table = None

        self.dimension = None

    def _set_dimension(self):
        if self.dimension is None and self.sec_mem_array is not None:
            self.dimension = len(self.sec_mem_array.shape)

    def get_latest_bar_value(self,
                             exchange: str,
                             asset_type: str,
                             symbol: str,
                             field: str):

        if asset_type == 'margin':
            asset_type = 'spot'

        try:
            symbol_idx = self.symbol_table[f'{exchange}.{asset_type}.{symbol}']
        except KeyError:
            return np.nan

        field_idx = self.field_table[field]

        self._set_dimension()

        if self.dimension == 3:
            return self.sec_mem_array[-1, symbol_idx, field_idx]
        elif self.dimension == 2:
            return self.sec_mem_array[symbol_idx, field_idx]




    # def get_latest_bar(self, exchange, asset_type, symbol, format='array'):
    #     # format: array, df, dict
    #     # curr_time = datetime.datetime.now().strftime('%H%M%S') if self.curr_time is None else self.curr_time
    #
    #     if asset_type == 'margin':
    #         asset_type = 'spot'
    #
    #     # data_array = np.array(self.sec_mem_array)
    #     # TODO :: Array로 바꾸는 속도 check 필요. 매번 바꿔주는 연산. Type Checker 활용?
    #
    #     if len(self.bartime_table):
    #         array = self.sec_mem_array[
    #            -1,
    #            self.symbol_table[f'{exchange}.{asset_type}.{symbol}'],
    #            :
    #         ]
    #     else:
    #         array = self.sec_mem_array[self.symbol_table[f'{exchange}.{asset_type}.{symbol}'], :]
    #
    #     if format == 'array':
    #         return array
    #     else:
    #         field_cnt = len(self.field_table)
    #         df = pd.DataFrame(array.reshape(-1, field_cnt), columns=list(self.field_table.keys()))
    #         df = df.ffill()
    #         if format == 'df':
    #             return df.iloc[-1]
    #         else:
    #             return df.iloc[-1].to_dict()
    #
    # def get_latest_bar_datetime(self):
    #     return datetime.datetime.now()
    #
    # def get_latest_N_bar_value(self, exchange, asset_type, symbol, N, field):
    #     try:
    #         # curr_time = datetime.datetime.now().strftime('%H%M%S') if self.curr_time is None else self.curr_time
    #
    #         # print(curr_time)
    #
    #         if asset_type == 'margin':
    #             asset_type = 'spot'
    #
    #         symbol_idx = self.symbol_table[f'{exchange}.{asset_type}.{symbol}']
    #         field_idx = self.field_table[field]
    #
    #         # data_array = np.array(self.sec_mem_array)
    #         # TODO :: Array로 바꾸는 속도 check 필요. 매번 바꿔주는 연산. Type Checker 활용?
    #
    #         if len(self.bartime_table):
    #             # backward_idx = self.bartime_table[curr_time] - N
    #             # backward_idx = 0 if backward_idx < 0 else backward_idx
    #
    #             # print(symbol, data_array[self.bartime_table[curr_time],
    #             #         symbol_idx, :])
    #
    #             return self.sec_mem_array[
    #                 -N:,
    #                 symbol_idx,
    #                 field_idx
    #             ]
    #         else:
    #             return self.sec_mem_array[symbol_idx, field_idx]
    #     except:
    #         import traceback
    #         traceback.print_exc()
    #         print(self.sec_mem_array)
    #
    # def get_latest_N_bar(self, exchange, asset_type, symbol, N, format='array'):
    #     # format: array, df, dict
    #     # curr_time = datetime.datetime.now().strftime('%H%M%S') if self.curr_time is None else self.curr_time
    #
    #     if asset_type == 'margin':
    #         asset_type = 'spot'
    #
    #     # data_array = np.array(self.sec_mem_array)
    #     # TODO :: Array로 바꾸는 속도 check 필요. 매번 바꿔주는 연산. Type Checker 활용?
    #
    #     if len(self.bartime_table):
    #         # backward_idx = self.bartime_table[curr_time] - N
    #         # backward_idx = 0 if backward_idx < 0 else backward_idx
    #         array = self.sec_mem_array[
    #            -N:,
    #            self.symbol_table[f'{exchange}.{asset_type}.{symbol}'],
    #            :
    #         ]
    #     else:
    #         array = self.sec_mem_array[self.symbol_table[f'{exchange}.{asset_type}.{symbol}'], :]
    #
    #     if format == 'array':
    #         return array
    #     else:
    #         field_cnt = len(self.field_table)
    #         df = pd.DataFrame(array.reshape(-1, field_cnt), columns=list(self.field_table.keys()))
    #         df = df.ffill()
    #         if format == 'df':
    #             return df.iloc[-1]
    #         else:
    #             return df.iloc[-1].to_dict()