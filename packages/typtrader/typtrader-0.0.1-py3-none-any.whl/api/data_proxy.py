from tradernetwork import (
    SubSocket,
    PubSocket,
    ProxySocket,
)

from params import (
    DATA_SERVER_HOST,
    DATA_SERVER_PORT,
    DATA_PROXY_MARKET_PORT,
    DATA_PROXY_ACCOUNT_PORT,
    DATA_PROXY_BAR_PORT,
)


class DataProxy:

    def __init__(self,
                 data_server_host: str = DATA_SERVER_HOST,
                 data_server_port: int = DATA_SERVER_PORT,
                 market_port: int = DATA_PROXY_MARKET_PORT,
                 account_port: int = DATA_PROXY_ACCOUNT_PORT,
                 bar_port: int = DATA_PROXY_BAR_PORT,
                 debug: bool = False):
        """
        외부에서 받은 데이터를 proxy하여 market, account, bar로 나누어 데이터를 뿌려주는 역할 (publish)

        :param data_server_host: 데이터 스트림을 받고 있는 서버 IP 주소 (외부)
        :param data_server_port: 데이터 스트림을 받는 서버의 포트 번호 (외부)
        :param market_port: trading tool에서 사용할 마켓 데이터 스트리밍 포트 (내부용)
        :param account_port: trading tool에서 사용할 어카운트 데이터 스트리밍 포트 (내부용)
        :param bar_port: trading tool에서 사용할 시간봉/분봉 데이터 스트리밍 포트 (내부용)
        :param debug: debug 모드를 True로 하면 외부로부터 받은 데이터를 프린트해준다. (DataProxy를 테스트하는 수단)
        """
        self.debug = debug

        self.market_pub_socket = PubSocket(market_port)
        self.account_pub_socket = PubSocket(account_port)
        self.bar_pub_socket = PubSocket(bar_port)

        # 현재 데이터는 2개 서버에서 모두 받을 수 있다.
        # 아래에는 하나의 서버만 연결하였지만, 필요에 따라서 모든 서버 혹은 다른 소스로부터 데이터를 추가로 받을 수도 있다.
        self.sockets = {
            'data': SubSocket(data_server_port, data_server_host),
        }

        self.proxy = ProxySocket(self.sockets)
        self.proxy.callback = self.callback

    def start_data_proxy_loop(self):
        print('Starting Data Proxy')
        self.proxy.start_proxy_server_loop()

    def callback(self, socket_name: str, data: dict):
        if self.debug:
            _ = socket_name
            print(data)

        source = data['source']

        if source in ['bybit_sec_svc', 'binance_sec_svc']:
            self.market_pub_socket.publish(data['data'])

        if source in ['bybit_account_svc', 'binance_account_svc_1', 'binance_account_svc_2']:
            self.account_pub_socket.publish(data['data'])

        if source in ['bybit_bar_svc']:
            self.bar_pub_socket.publish(data['data'])


if __name__ == '__main__':
    server = DataProxy(debug=False)
    server.start_data_proxy_loop()
