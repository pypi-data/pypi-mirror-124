import os
from typing import List
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
application = get_wsgi_application()

from db.models import User, Strategy
from cryptography.fernet import Fernet
from django.contrib.auth.hashers import check_password

load_dotenv(override=True)

IS_DOCKER = bool(int(os.getenv('DOCKER', 0)))

redis_default_params = {
    'redis_host': os.getenv('REDIS_HOST'),
    'redis_port': os.getenv('REDIS_PORT'),
    'redis_password': os.getenv('REDIS_PW')
}

influxdb_default_params = {
    'influxdb_host': os.getenv('INFLUXDB_HOST'),
    'influxdb_token': os.getenv('INFLUXDB_TOKEN'),
    'influxdb_org': os.getenv('INFLUXDB_ORG'),
    'influxdb_bucket': os.getenv('INFLUXDB_BUCKET')
}

data_proxy_default_params = {
    'data_server_host': os.getenv('SERVER_1_HOST'),
    'data_server_port': 4011,
    'data_proxy_host': 'localhost',
    'data_proxy_market_port': 12000,
    'data_proxy_account_port': 12001,
    'data_proxy_bar_port': 12002
}

STRATEGY_INFO = {
    'ppark9553@gmail.com': {
        'default': {
            'category': 'crypto',
            'description': 'default crypto strategy',
            'init_time': '20211015',
            'active': True,
            'skip_missed': True,
            'use_frames': 'hour',
            **redis_default_params,
            **influxdb_default_params,
            **data_proxy_default_params,
            'strategy_queue_host': 'localhost' if not IS_DOCKER else 'host.docker.internal',
            'strategy_queue_port': 12999,
            'order_queue_host': 'localhost' if not IS_DOCKER else 'host.docker.internal',
            'order_queue_port': 15999,
            'execution_queue_host': 'localhost' if not IS_DOCKER else 'host.docker.internal',
            'execution_queue_port': 12006,
            'binance_public_key': os.getenv('PP_BINANCE_PUBLIC_KEY'),
            'binance_private_key': os.getenv('PP_BINANCE_SECRET_KEY'),
            'bybit_public_key': os.getenv('COIN_ARBIT_BYBIT_PUBLIC_KEY'),
            'bybit_private_key': os.getenv('COIN_ARBIT_BYBIT_PRIVATE_KEY'),
            'upbit_public_key': None,
            'upbit_private_key': None,
        },
        'example': {
            'category': 'crypto',
            'description': 'example crypto strategy',
            'init_time': '20211015',
            'active': True,
            'skip_missed': True,
            'use_frames': 'hour',
            **redis_default_params,
            **influxdb_default_params,
            **data_proxy_default_params,
            'strategy_queue_host': 'localhost' if not IS_DOCKER else 'host.docker.internal',
            'strategy_queue_port': 12999,
            'order_queue_host': 'localhost' if not IS_DOCKER else 'host.docker.internal',
            'order_queue_port': 15999,
            'execution_queue_host': 'localhost' if not IS_DOCKER else 'host.docker.internal',
            'execution_queue_port': 12006,
            'binance_public_key': os.getenv('PP_BINANCE_PUBLIC_KEY'),
            'binance_private_key': os.getenv('PP_BINANCE_SECRET_KEY'),
            'bybit_public_key': os.getenv('COIN_ARBIT_BYBIT_PUBLIC_KEY'),
            'bybit_private_key': os.getenv('COIN_ARBIT_BYBIT_PRIVATE_KEY'),
            'upbit_public_key': None,
            'upbit_private_key': None,
        },
    }
}


def create_strategy_info(username: str,
                         password: str,
                         strategy_id: str,
                         st_info: dict = None):
    if st_info is None:
        try:
            st_info = STRATEGY_INFO[username][strategy_id]
        except:
            raise Exception('No matching username or strategy_id. Check again.')

    user = User.objects.filter(email=username).first()
    auth = check_password(password, user.password)

    if auth:
        no_encrypt_field = ['name', 'category', 'description', 'init_time',
                            'active', 'skip_missed', 'user_frames', 'encrypt_key']

        """
        단순하게 key를 generate하는 방식이 아니라,
        generate한 key에 비밀번호를 더해서 key로 사용
        """
        key = Fernet.generate_key()
        st_info['encrypt_key'] = key.decode('utf-8')
        key = (key.decode('utf-8') + password).encode('utf-8')
        cipher_suite = Fernet(key)

        for field, value in st_info.items():
            if field not in no_encrypt_field:
                v = str(value).encode('utf-8')
                cipher_text = cipher_suite.encrypt(v)
                st_info[field] = cipher_text.decode('utf-8')

        st_info['name'] = strategy_id
        st_info['owner'] = user
        st_info['user'] = user

        st_inst = Strategy(**st_info)
        st_inst.save()
        return st_inst
    else:
        raise Exception('User authentication failed. Username/Password did not match.')


def get_strategy_info(username: str,
                      password: str,
                      strategy_id: str,
                      st_info: dict = None):
    if st_info is None:
        user = User.objects.filter(email=username).first()
        auth = check_password(password, user.password)
        if auth:
            no_encrypt_field = ['id', 'owner_id', 'user_id', 'name', 'category', 'description', 'init_time',
                                'active', 'skip_missed', 'universe_id', 'user_frames', 'encrypt_key',
                                'created', 'updated']

            s = Strategy.objects.filter(user=user, name=strategy_id).first()
            if s is not None:
                st_info = s.__dict__
                _ = st_info.pop('_state')
                key = (st_info['encrypt_key'] + password).encode('utf-8')
                cipher_suite = Fernet(key)
                for field, value in st_info.items():
                    if field not in no_encrypt_field:
                        st_info[field] = cipher_suite.decrypt(value.encode('utf-8')).decode('utf-8')
                        if 'port' in field:
                            st_info[field] = int(st_info[field])
                return st_info
            else:
                raise Exception('No such strategy_id.')
        else:
            raise Exception('User authentication failed. Username/Password did not match.')
    else:
        return st_info


def generate_execution_params(username: str,
                              password: str,
                              strategy_id: str,
                              st_info: dict = None,
                              debug: bool = False):
    st_info = get_strategy_info(username=username,
                                password=password,
                                strategy_id=strategy_id,
                                st_info=st_info)
    params = {
        'account_handler_params': {
            'jango_req_time': 60 * 10,
            'execution_host': st_info['execution_queue_host'],
            'execution_port': st_info['execution_queue_port'],
            'strategy_ls': [strategy_id],
            'debug': debug,
        },
        'holdings_tracker_params': {
            'update_time': 30,
            'redis_host': st_info['redis_host'],
            'redis_port': st_info['redis_port'],
            'redis_password': st_info['redis_password'],
            'influxdb_host': st_info['influxdb_host'],
            'influxdb_token': st_info['influxdb_token'],
            'influxdb_org': st_info['influxdb_org'],
            'influxdb_bucket': st_info['influxdb_bucket'],
            'strategy_ls': [strategy_id],
            'debug': debug,
        },
        'order_handler_params': {
            'order_host': st_info['order_queue_host'],
            'order_port': st_info['order_queue_port'],
            'execution_host': st_info['execution_queue_host'],
            'execution_port': st_info['execution_queue_port'],
            'strategy_ls': [strategy_id],
            'debug': debug,
        },
        'execution_handler_params': {
            'execution_host': st_info['execution_queue_host'],
            'execution_port': st_info['execution_queue_port'],
            'strategy_host': st_info['strategy_queue_host'],
            'strategy_ports': {strategy_id: st_info['strategy_queue_port']},
            'order_host': st_info['order_queue_host'],
            'order_ports': {strategy_id: st_info['order_queue_port']},
            'redis_host': st_info['redis_host'],
            'redis_port': st_info['redis_port'],
            'redis_password': st_info['redis_password'],
            'strategy_ls': [strategy_id],
            'debug': debug,
        },
    }
    return params


def generate_bulk_account_execution_params(username: str,
                                           password: str,
                                           strategy_ls: List[str],
                                           strategy_info: dict = None,
                                           debug: bool = False):

    strategy_ports = {st: None for st in strategy_ls}
    order_ports = {st: None for st in strategy_ls}

    params = None

    for st in strategy_ls:
        if strategy_info is not None:
            st_info = strategy_info[username][st]
        else:
            st_info = None
        params = generate_execution_params(username=username,
                                           password=password,
                                           strategy_id=st,
                                           st_info=st_info,
                                           debug=debug)
        execution_handler_params = params['execution_handler_params']
        strategy_ports[st] = execution_handler_params['strategy_ports'][st]
        order_ports[st] = execution_handler_params['order_ports'][st]

    bulk_params = {
        'account_handler_params': params['account_handler_params'],
        'holdings_tracker_params': params['holdings_tracker_params'],
        'execution_handler_params': params['execution_handler_params']
    }
    bulk_params['account_handler_params']['strategy_ls'] = strategy_ls
    bulk_params['holdings_tracker_params']['strategy_ls'] = strategy_ls
    bulk_params['execution_handler_params']['strategy_ports'] = strategy_ports
    bulk_params['execution_handler_params']['order_ports'] = order_ports
    bulk_params['execution_handler_params']['strategy_ls'] = strategy_ls
    return bulk_params


if __name__ == '__main__':
    # create_strategy_info('coin.trader.korea@gmail.com', '123123', 'default')

    # params = generate_execution_params('coin.trader.korea@gmail.com', '123123', 'default')
    # print(params)

    params = generate_bulk_account_execution_params('coin.trader.korea@gmail.com',
                                                    '123123',
                                                    ['example'],
                                                    STRATEGY_INFO)
    print(params)