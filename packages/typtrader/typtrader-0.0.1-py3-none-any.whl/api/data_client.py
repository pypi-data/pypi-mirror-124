import datetime
import threading
import numpy as np
from functools import partial
from typing import Callable, Dict
from tradernetwork import SubSocket

from engine.utils.log import CoinTelegram
from api.docker_handler import DockerHandler


class DataClient:

    def __init__(self,
                 market_host: str = 'localhost',
                 market_port: int = 12000,
                 account_host: str = 'localhost',
                 account_port: int = 12001,
                 bar_host: str = 'localhost',
                 bar_port: int = 12002,
                 debug: bool = False):
        """
        data_proxy에서 실행한 DataProxy에서 스트리밍 받은 데이터를 DataHandler로 보내주는 역할 수행
        데이터가 안 들어오기 시작하면 텔레그램으로 오류를 보내고 데이터가 스트리밍되고 있는 도커 컨테이너 재시작하기.

        :param market_host: DataProxy가 돌아가고 있는 서버
        :param market_port: DataProxy market_port와 동일
        :param account_host: DataProxy가 돌아가고 있는 서버
        :param account_port: DataProxy account_port와 동일
        :param bar_host: DataProxy가 돌아가고 있는 서버
        :param bar_port: DataProxy bar_port와 동일
        :param debug: debug모드로 실행하면 도커는 재시작하지 않는다
        """

        self.debug = debug

        if not self.debug:
            """
            debug모드가 아닐 경우 실제로 텔레그램 메세지와 함께 도커를 재시작할 수 있도록 한다.
            
            도커를 재시작하기 위해서는 꼭 worker server에서 server가 실행되어 있어야 한다. (ZeroMQ기반 Request 서버)
            그 이유는 도커를 재시작하기 위해서 도커 API를 직접 컨트롤하지 않고 worker server에서 Celery 워커가 Fabric을 사용해서
            도커를 재시작하기 때문이다. 이렇게 하는 이유는 비동기적으로 태스크를 분배하고 그 태스크의 상태를 쉽게 파악하기 위함이다.
            """
            self.docker_handler = DockerHandler()
        else:
            self.docker_handler = None

        self.telegram = CoinTelegram(debug=self.debug)

        self.market_conn = SubSocket(market_port, market_host)
        self.account_conn = SubSocket(account_port, account_host)
        self.bar_conn = SubSocket(bar_port, bar_host)

        self.callback = None

        # 실시간 데이터를 담아두는 딕셔너리
        # 데이터가 끊겨서 데이터를 받고 있지 않은 경우 모든 필드값을 np.nan으로 채워서 publish해주기 위함
        self.current_data: Dict[str, dict] = {'market': {},
                                              'account': {},
                                              'bar': {}}

        self.data_status: Dict[str, Dict[str, datetime]] = {'market': {'binance': None, 'bybit': None},
                                                            'account': {'binance': None, 'bybit': None},
                                                            'bar': {'bybit': None}}

        self.telegram_msg_sent: Dict[str, Dict[str, bool]] = {'market': {'binance': False, 'bybit': False},
                                                              'account': {'binance': False, 'bybit': False},
                                                              'bar': {'bybit': False}}

        self._healthcheck_loop()

    def _stream_data(self, data_type: str, callback: Callable):
        self.callback = callback
        callback_func = partial(self.callback_wrapper,
                                data_type=data_type,
                                callback=self.callback)

        if data_type == 'market':
            sock = self.market_conn
        elif data_type == 'account':
            sock = self.account_conn
        elif data_type == 'bar':
            sock = self.bar_conn
        while True:
            data = sock._recv()
            callback_func(data)

    def callback_wrapper(self, data: dict, data_type: str, callback: Callable):
        if data_type == 'market':
            source = data['source']
            symbol = data['symbol']
            key = f'{source}.{symbol}'

            if self.telegram_msg_sent['market'][source]:
                time_fmt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                tele_msg = '[Data Client]\n' \
                           '🔅 MARKET DATA STREAM RESTARTED 🔅\n' \
                           f'{source.upper()} has restarted streaming since:\n' \
                           f'{time_fmt}'
                self.telegram.send_msg(tele_msg)

            self.current_data['market'][key] = data
            self.data_status['market'][source] = datetime.datetime.now()
            self.telegram_msg_sent['market'][source] = False

        # client가 설정한 callback함수 실행시키기
        callback(data)

    def stream_market_data(self, callback: Callable):
        t = threading.Thread(target=self._stream_data, args=('market', callback))
        t.start()

    def stream_account_data(self, callback: Callable):
        t = threading.Thread(target=self._stream_data, args=('account', callback))
        t.start()

    def stream_bar_data(self, callback: Callable):
        t = threading.Thread(target=self._stream_data, args=('bar', callback))
        t.start()

    def _healthcheck_loop(self):
        time_now = datetime.datetime.now()

        """
        TODO::
        추후 account/bar 소켓도 테스트하는 로직을 구현할 필요가 있다.
        """

        # 마켓 데이터를 확인하는 섹션
        for source, status in self.data_status['market'].items():
            if status is not None and (time_now - status).seconds >= 5:
                for key in self.current_data['market'].keys():
                    if key.split('.')[0] == source:
                        data = self.current_data['market'][key]['data']
                        empty_data = {data_key: np.nan for data_key, _ in data.items()}
                        self.current_data['market'][key]['data'] = empty_data
                        self.callback(self.current_data['market'][key])

                if not self.telegram_msg_sent['market'][source]:
                    status_fmt = status.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                    tele_msg = '[Data Client]\n' \
                               '📛 MARKET DATA STREAM STOPPED 📛\n' \
                               f'{source.upper()} has stopped streaming since:\n' \
                               f'{status_fmt}'
                    self.telegram.send_msg(tele_msg)
                    self.telegram_msg_sent['market'][source] = True

                    # 텔레그램 메세지를 전송했다면, 데이터 스트리밍이 되고 있는 도커 컨테이너를 재시작해줘야 한다. (참고로 재시작을 해도 안 되는 경우가 있다.)
                    # 재시작을 했는데도 안 되는 경우에는 조금 기다렸다가 사람이 직접(수동으로) 컨테이너를 재시작해야 한다.
                    if self.docker_handler is not None:
                        if source == 'bybit':
                            containers = ['bybit_market_svc']
                        elif source == 'binance':
                            containers = ['binance_market_svc_1', 'binance_market_svc_2']
                        else:
                            containers = []

                        for server in [1, 2]:
                            for container in containers:
                                task_id = self.docker_handler.restart(server, container)
                                tele_msg = '[Data Client]\n' \
                                           f'⚙️ DOCKER AUTO RESTARTING: {container}.\n' \
                                           'Check URL below 👇\n\n' \
                                           f'Task Link: https://task.blended.kr/task/{task_id}'
                                print(tele_msg)
                                self.telegram.send_msg(tele_msg)

        timer = threading.Timer(5, self._healthcheck_loop)
        timer.setDaemon(True)
        timer.start()


if __name__ == '__main__':
    client = DataClient(debug=False)


    def print_crypto_data(data):
        print(data)


    client.stream_bar_data(callback=print_crypto_data)