from typing import Dict, List
from multiprocessing import Queue
from cointraderkr import MIN_TRADE_AMOUNT

from engine.utils.log import Logger
from engine.events import OrderSuccessEvent
from engine.execution_v2.portfolio import Portfolio
from engine.utils.distributed_queue import DistributedQueue
from params import (
    EXECUTION_QUEUE_HOST,
    EXECUTION_QUEUE_PORT,
    STRATEGY_QUEUE_HOST,
    EXAMPLE_STRATEGY_QUEUE_PORT,
    ORDER_QUEUE_HOST,
    EXAMPLE_ORDER_QUEUE_PORT,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PASSWORD,
)

STRATEGY_LS = ['example']

STRATEGY_PORTS = {
    'example': EXAMPLE_STRATEGY_QUEUE_PORT
}

ORDER_PORTS = {
    'example': EXAMPLE_ORDER_QUEUE_PORT
}


class ExecutionHandler:

    def __init__(self,
                 execution_host: str = EXECUTION_QUEUE_HOST,
                 execution_port: int = EXECUTION_QUEUE_PORT,
                 execution_queue: Queue = None,
                 strategy_host: str = STRATEGY_QUEUE_HOST,
                 strategy_ports: Dict[str, int] = STRATEGY_PORTS,
                 strategy_queues: Dict[str, Queue] = None,
                 order_host: str = ORDER_QUEUE_HOST,
                 order_ports: Dict[str, int] = ORDER_PORTS,
                 order_queues: Dict[str, Queue] = None,
                 redis_host: str = REDIS_HOST,
                 redis_port: int = REDIS_PORT,
                 redis_password: str = REDIS_PASSWORD,
                 port_cls: Portfolio = None,
                 strategy_ls: List[str] = STRATEGY_LS,
                 backtest: bool = False,
                 debug: bool = False):

        self.debug = debug
        self.backtest = backtest

        self.execution_host = execution_host
        self.execution_port = execution_port

        if execution_queue is None:
            self.execution_queue = DistributedQueue(execution_port, execution_host)
            print(f'[Execution] Created Execution DistributedQueue at tcp://{execution_host}:{execution_port}')
        else:
            self.execution_queue = execution_queue

        if strategy_queues is None:
            self.strategy_queues = {st: DistributedQueue(st_port, strategy_host)
                                    for st, st_port in strategy_ports.items()}
            print(f'[Execution] Created Strategy DistributedQueues')
        else:
            self.strategy_queues = strategy_queues

        if order_queues is None:
            self.order_queues = {st: DistributedQueue(o_port, order_host)
                                 for st, o_port in order_ports.items()}
            print(f'[Execution] Created Order DistributedQueues')
        else:
            self.order_queues = order_queues

        self.logger = Logger(debug=debug)

        if backtest:
            self.portfolio = port_cls
        else:
            self.portfolio = Portfolio(execution_host=execution_host,
                                       execution_port=execution_port,
                                       execution_queue=execution_queue,
                                       strategy_host=strategy_host,
                                       strategy_ports=strategy_ports,
                                       strategy_queues=strategy_queues,
                                       redis_host=redis_host,
                                       redis_port=redis_port,
                                       redis_password=redis_password,
                                       strategy_ls=strategy_ls,
                                       backtest=backtest,
                                       debug=debug)

        self.minimum_trade_amount = MIN_TRADE_AMOUNT

        # Order Table(원장)
        self.strategy_ls = strategy_ls
        self.order_table = self.portfolio.order_table

    def handle_order_success(self, event: OrderSuccessEvent):
        strategy_id = event.strategy_id
        order_uid = event.order_uid
        status = event.status

        if order_uid in self.order_table[strategy_id]:
            if status == 'SUCCESS':
                if order_uid in self.order_table[strategy_id]:
                    self.order_table[strategy_id].pop(order_uid)
                    self.portfolio.save_order_table()
                    event.save()
                    self.logger.info(f'[Execution] {event.strategy_id} ORDER SUCCESS: {event.order_uid}')
                    self.strategy_queues[strategy_id].put(event)
            elif status == 'FAIL':
                # retry order
                order_event = self.order_table[strategy_id][order_uid]
                if order_event.retry:
                    if (order_event.retry_num - order_event.retry_cnt) > 0:
                        order_event.retry_cnt = order_event.retry_cnt + 1
                        self.execution_queue.put(order_event)
                        event.save()
                        log_msg = f'[Execution] {event.strategy_id} ORDER FAIL: RETRYING ({order_event.retry_cnt}/{order_event.retry_num}) {event.order_uid}'
                        self.logger.info(log_msg)
                else:
                    self.strategy_queues[strategy_id].put(event)

    def start_execution_loop(self):
        while True:
            event = self.execution_queue.get()

            if event.type == 'JANGO' or self.portfolio.jango_updated or self.debug:

                if event.type == 'JANGO':
                    msg = event.message(module='Execution')
                    self.logger.info(msg)
                    self.portfolio.update_jango(event, method='self_update')

                if event.type == 'ORDER':
                    """
                    OrderEvent는 Execution에서 핸들링하지 않고 전략별로
                    OrderHandler를 따로 둔 곳으로 이벤트를 전달해준다.
                    """
                    msg = event.message(module='Execution')
                    self.logger.info(msg)
                    self.portfolio.handle_order_event(event)
                    strategy_id = event.strategy_id
                    self.order_queues[strategy_id].put(event)

                elif event.type == 'FILL':
                    msg = event.message(module='Execution')
                    self.logger.info(msg)
                    self.portfolio.handle_fill_event(event)

                elif event.type == 'ORDER_SUCCESS':
                    msg = event.message(module='Execution')
                    self.logger.info(msg)
                    self.handle_order_success(event)


def start_account():
    from engine.execution_v2.account import AccountHandler
    a = AccountHandler(debug=True)
    a.start_account_loop()


def start_order():
    from engine.execution_v2.order import CryptoOrderHandler
    o = CryptoOrderHandler(debug=True)
    o.start_order_loop()


if __name__ == '__main__':
    import time
    from multiprocessing import Process

    from engine.events import SignalEvent

    ap = Process(target=start_account)
    ap.start()

    op = Process(target=start_order)
    op.start()

    time.sleep(5)

    eh = ExecutionHandler(debug=True)
    eh.start_execution_loop()
