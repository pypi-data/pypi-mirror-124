import json
import redis
import pandas as pd
import zstandard as zstd
from sqlalchemy import create_engine, inspect

from app.settings import (
    DATABASES,
    CACHES,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PW,
)


class DBHandler:

    def __init__(self):
        if DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
            db_path = DATABASES['default']['NAME']
            self.db = create_engine(f'sqlite:///{db_path}')
            self.inspector = inspect(self.db)
            self.tables = self.inspector.get_table_names()

        if CACHES['default']['BACKEND'] == 'django_redis.cache.RedisCache':
            self.cache = redis.StrictRedis(host=REDIS_HOST,
                                           port=REDIS_PORT,
                                           password=REDIS_PW)

    def read_data(self, tablename: str) -> pd.DataFrame:
        if tablename in self.tables:
            return pd.read_sql(tablename, self.db)

    def get_hour_data(self, symbol_id: str = None) -> pd.DataFrame:
        data = self.read_data('db_cryptohourdata')
        if symbol_id is None:
            return data.drop('id', axis=1).reset_index(drop=True)
        else:
            df = data[data['symbol_id'] == symbol_id]
            return df.drop('id', axis=1).reset_index(drop=True)

    def get_cached_hour_data(self, symbol_id: str):
        d = zstd.ZstdDecompressor()
        cached = self.cache.get(symbol_id)
        decompressed = d.decompress(cached)
        data_json = json.loads(decompressed)
        data = pd.DataFrame(data_json)
        return data

    def cache_hour_data(self):
        data = self.get_hour_data()
        symbol_ids = set(data['symbol_id'])
        c = zstd.ZstdCompressor()
        for symbol_id in symbol_ids:
            symbol_data = data[data['symbol_id'] == symbol_id]
            data_bytes = symbol_data.to_json().encode('utf-8')
            compressed = c.compress(data_bytes)
            self.cache.set(symbol_id, compressed)
            print(f'{symbol_id} cached complete.')


if __name__ == '__main__':
    import time

    db = DBHandler()

    s = time.time()
    data = db.get_cached_hour_data('bybit_usdt_BTCUSDT')
    e = time.time()
    print(e - s)

    s = time.time()
    data = db.get_hour_data('bybit_usdt_BTCUSDT')
    e = time.time()
    print(e - s)