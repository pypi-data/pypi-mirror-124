import os
import pickle
from typing import Any
from pathlib import Path

ENGINE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
PERSIST_DIR = ENGINE_DIR.parent.parent / 'persist_db'

os.makedirs(PERSIST_DIR, exist_ok=True)


class PersistDB:
    """
    툴이 꺼져도 persist해야 하는 데이터를 피클하여 저장하는 역할 수행

    툴을 재실행하면 기존에 저장되어 있던 파일을 불러온다.
    """

    def __init__(self):
        self.path = PERSIST_DIR

    def set(self, name: str, data: Any):
        with open(self.path / f'{name}.pkl', 'wb') as f:
            pickle.dump(data, f)

    def get(self, name: str, default: Any = None):
        data_name = f'{name}.pkl'
        if os.path.exists(self.path / data_name):
            with open(self.path / f'{name}.pkl', 'rb') as f:
                data = pickle.load(f)
            return data
        else:
            return default


if __name__ == '__main__':
    from collections import OrderedDict

    d = OrderedDict()
    d['test1'] = 1
    d['test2'] = 2

    db = PersistDB()
    db.set('test', d)

    data = db.get('test')
    print(data)

    data = db.get('test1', {})
    print(data)