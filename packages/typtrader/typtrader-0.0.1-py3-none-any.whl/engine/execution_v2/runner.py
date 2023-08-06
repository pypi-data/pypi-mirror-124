from typing import List
from multiprocessing import Process

from engine.execution_v2.account import AccountHandler
from engine.execution_v2.order import CryptoOrderHandler
from engine.execution_v2.execution import ExecutionHandler
from engine.execution_v2.holdings_tracker import HoldingsTracker
from operations.strategy_info import (
    generate_execution_params,
    generate_bulk_account_execution_params,
)


class ExecutionRunner:

    def __init__(self,
                 username: str,
                 password: str,
                 account_handler_params: dict = None,
                 holdings_tracker_params: dict = None,
                 execution_handler_params: dict = None,
                 debug: bool = False):

        self.username = username
        self.password = password
        self.debug = debug

        self.account_handler_params = None if account_handler_params is None else account_handler_params
        self.holdings_tracker_params = None if holdings_tracker_params is None else holdings_tracker_params
        self.execution_handler_params = None if execution_handler_params is None else execution_handler_params

    def _account_handler_process(self):
        ah = AccountHandler(**self.account_handler_params)
        ah.start_account_loop()

    def _holdings_tracker_process(self):
        ht = HoldingsTracker(**self.holdings_tracker_params)
        ht.start_holdings_tracker_loop()

    def _order_handler_process(self, params: dict):
        oh = CryptoOrderHandler(**params)
        oh.start_order_loop()

    def _execution_handler_process(self):
        eh = ExecutionHandler(**self.execution_handler_params)
        eh.start_execution_loop()

    def start(self,
              strategy_ls: List[str],
              run: List[str] = ['account_handler',
                                'holdings_tracker',
                                'order_handler',
                                'execution_handler']):

        bulk_params = generate_bulk_account_execution_params(username=self.username,
                                                             password=self.password,
                                                             strategy_ls=strategy_ls,
                                                             debug=self.debug)

        params = {
            st: generate_execution_params(username=self.username,
                                          password=self.password,
                                          strategy_id=st,
                                          debug=self.debug)['order_handler_params']
            for st in strategy_ls
        }

        if self.account_handler_params is None:
            self.account_handler_params = bulk_params['account_handler_params']
        if self.holdings_tracker_params is None:
            self.holdings_tracker_params = bulk_params['holdings_tracker_params']
        if self.execution_handler_params is None:
            self.execution_handler_params = bulk_params['execution_handler_params']

        if 'account_handler' in run:
            ahp = Process(target=self._account_handler_process)
            ahp.start()

        if 'holdings_tracker' in run:
            htp = Process(target=self._holdings_tracker_process)
            htp.start()

        if 'order_handler' in run:
            for _, param in params.items():
                p = Process(target=self._order_handler_process, args=(param,))
                p.start()

        if 'execution_handler' in run:
            ehp = Process(target=self._execution_handler_process)
            ehp.start()


if __name__ == '__main__':
    runner = ExecutionRunner('coin.trader.korea@gmail.com', '123123', debug=True)
    runner.start(strategy_ls=['example'],
                 run=['account_handler', 'holdings_tracker', 'order_handler', 'execution_handler'])
