import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
application = get_wsgi_application()

import time
from db.models import (
    User,
    Symbol,
    Universe,
    Strategy,
    CryptoMinuteData,
    CryptoHourData,
)
from params import (
    EXCHANGE_LIST,
    ASSET_LIST,
    SYMBOL_LIST,
)
from api.bar_deque import get_bybit_usdt_futures_data
from operations.strategy_info import STRATEGY_INFO, create_strategy_info


def db_init_setup():
    admin_email = 'ppark9553@gmail.com'
    admin_password = 'random123123'

    u = User.objects.get(email=admin_email)

    # STEP #1: 유니버스를 구성할 symbol 등록하기
    symbols = []
    for e in EXCHANGE_LIST:
        for a in ASSET_LIST:
            for s in SYMBOL_LIST:
                if e == 'bybit':
                    id = f'{e}_{a}_{s}'
                    if not Symbol.objects.filter(symbol_id=id).exists():
                        symbol = Symbol(exchange=e,
                                        asset_type=a,
                                        symbol=s,
                                        symbol_id=id,
                                        active=True)
                        symbol.save()
                    else:
                        symbol = Symbol.objects.filter(symbol_id=id).first()
                    symbols.append(symbol)

    # STEP #2: 전략에서 사용할 universe 구성하기
    if not Universe.objects.filter(owner=u, name='bybit_usdt_universe').exists():
        bybit_usdt_univ = Universe(owner=u, name='bybit_usdt_universe', public=True)
        bybit_usdt_univ.save()

        for symbol in symbols:
            if symbol.exchange == 'bybit' and symbol.asset_type == 'usdt':
                bybit_usdt_univ.symbols.add(symbol)
    else:
        bybit_usdt_univ = Universe.objects.filter(owner=u, name='bybit_usdt_universe').first()

    # STEP #3: 유저의 전략 생성
    for st, st_info in STRATEGY_INFO[admin_email].items():
        if not Strategy.objects.filter(owner=u, name=st).exists():
            strategy = create_strategy_info(username=admin_email,
                                            password=admin_password,
                                            strategy_id=st)
        else:
            strategy = Strategy.objects.filter(owner=u, name=st).first()

        strategy.universe = bybit_usdt_univ
        strategy.save()

    # STEP #4: 가격 데이터 저장
    for symbol in bybit_usdt_univ.symbols.all():
        for interval in ['1m', '60m']:
            s = time.time()
            data = get_bybit_usdt_futures_data(symbol.symbol, interval, maxlen=10000)
            e = time.time()
            print(f'{symbol} {interval} request done in: {e - s} seconds.')
            data_dict = data.T.to_dict()
            bulk_list = []
            model = CryptoMinuteData if interval == '1m' else CryptoHourData
            done_dates = list(set(model.objects.filter(symbol=symbol.symbol).values_list('date', flat=True)))
            for _, data_row in data_dict.items():
                date = data_row['start_at'].strftime('%Y%m%d%H%M%S')
                if date not in done_dates:
                    d_pt = model(exchange='bybit',
                                 asset_type='usdt',
                                 symbol=symbol.symbol,
                                 symbol_id=f'bybit_usdt_{symbol.symbol}',
                                 date=date,
                                 open_prc=float(data_row['open']),
                                 high_prc=float(data_row['high']),
                                 low_prc=float(data_row['low']),
                                 close_prc=float(data_row['close']),
                                 volume=float(data_row['volume']))
                    bulk_list.append(d_pt)
            model.objects.bulk_create(bulk_list)
            print(f'Save {symbol} {interval} data done. Saved: {len(bulk_list)}')


if __name__ == '__main__':
    db_init_setup()