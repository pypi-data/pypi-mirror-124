from typing import Any
from tradernetwork import PushSocket, PullSocket

import engine.events as EVENTS


class AttrDict(dict):
    """
    딕셔너리를 인자값으로 받아서 클래스 property처럼 사용할 수 있도록 해주는 class wrapper
    """

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class DistributedQueue:
    """
    일반 Queue와 같은 put, get을 할 수 있다.
    하지만, 소켓 통신을 기반으로 한 큐이기 때문에 주고 받을 수 있는 데이터는 철저히 JSON이다.
    데이터를 클래스 객체로 받아서는 클래스명을 붙여서 데이터를 보내면 데이터를 받는 쪽에서는 이를 객체로
    반환하여 리턴한다.
    """

    def __init__(self, port: int, host: str = 'localhost'):
        self.host = host
        self.port = port

        self.push_socket = PushSocket(port, host)
        self.pull_socket = None

    def _make_pull_socket(self):
        self.pull_socket = PullSocket(self.port, self.host)

    def put(self, data: Any):
        if isinstance(data, EVENTS.Event):
            cls = data.__class__.__name__
            data_dict = data.__dict__
            data = {'cls': cls, 'data': data_dict}
        self.push_socket.publish(data)

    def get(self):
        if self.pull_socket is None:
            self._make_pull_socket()
        data = self.pull_socket._recv()
        if 'cls' in data:
            cls = getattr(EVENTS, data['cls'])
            data = cls(**data['data'])
        else:
            data = AttrDict(data)
        return data


if __name__ == '__main__':
    from engine.events import PairOrderEvent

    q = DistributedQueue(1001)

    evt = PairOrderEvent(1, 2)
    q.put(evt)

    qq = DistributedQueue(1001)
    data = q.get()
    print(data)

