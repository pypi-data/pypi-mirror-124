import os
import json
import telepot
import logging
import datetime
import traceback
from pathlib import Path
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
application = get_wsgi_application()

from db.models import Log

load_dotenv(override=True)

CURR_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = int(os.getenv('TELEGRAM_CHAT_ID', 0))


class CoinTelegram:
    """
    코인 트레이딩 시스템 전용 텔레그램 메세지 핸들러
    """

    def __init__(self,
                 id: int = TELEGRAM_CHAT_ID,
                 token: str = TELEGRAM_TOKEN,
                 debug: bool = False):
        self.bot = telepot.Bot(token)
        self.chat_id = id
        self.tele_err_cnt = 0
        self.debug = debug

    def send_msg(self, txt: str):
        try:
            if self.debug:
                txt = f'[DEBUG]' \
                      f'{txt}'
            self.bot.sendMessage(chat_id=self.chat_id, text=txt)
        except:
            self.tele_err_cnt += 1
            traceback.print_exc()
            print(f'Telegram send msg failed...! {self.tele_err_cnt}')


class DebugLogger(logging.Logger):

    log_path = CURR_DIR.parent.parent / 'logs'

    def __init__(self, name: str = 'debug_logger'):
        super().__init__(name)

        today = datetime.datetime.now().strftime('%Y%m%d')
        os.makedirs(self.log_path, exist_ok=True)

        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(self.log_path / f'{name}_{today}.log')

        fmt = f'[%(levelname)s] %(asctime)s %(message)s'
        formatter = logging.Formatter(fmt)

        stream_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        self.addHandler(stream_handler)
        self.addHandler(file_handler)

        self.setLevel(level=logging.DEBUG)


class TraderLogHandler(logging.StreamHandler):

    def __init__(self,
                 username: str,
                 strategy_id: str,
                 source: str = 'trader_logger',
                 ip_address: str = '127.0.0.1'):

        super().__init__()

        self.username = username
        self.strategy_id = strategy_id
        self.source = source
        self.ip_address = ip_address

        fmt = {
            'username': self.username,
            'strategy_id': self.strategy_id,
            'source': self.source,
            'ip_address': self.ip_address,
            'log_level': '%(levelname)s',
            'message': '%(message)s'
        }
        formatter = logging.Formatter(json.dumps(fmt))
        self.setFormatter(formatter)

    def emit(self, record):
        data = json.loads(self.format(record))
        Log(**data).stream_save()


class TraderLogger:

    def __init__(self,
                 username: str = 'coin.trader.korea@gmail.com',
                 strategy_id: str = 'all_strategies',
                 source: str = 'trader_logger',
                 ip_address: str = '127.0.0.1',
                 print_log: bool = False):

        self.print_log = print_log

        self.logger = logging.getLogger(source)
        self.logger.setLevel(logging.DEBUG)

        handler = TraderLogHandler(username=username,
                                   strategy_id=strategy_id,
                                   source=source,
                                   ip_address=ip_address)
        self.logger.addHandler(handler)

    def debug(self, log: str):
        if self.print_log:
            print(log)
        if log is not None:
            log = log.replace('\n', '\\n')
            self.logger.debug(log)

    def info(self, log: str):
        if self.print_log:
            print(log)
        if log is not None:
            log = log.replace('\n', '\\n')
            self.logger.info(log)

    def error(self, log: str):
        if self.print_log:
            print(log)
        if log is not None:
            log = log.replace('\n', '\\n')
            self.logger.error(log)

    def exception(self, log: str):
        if self.print_log:
            print(log)
        if log is not None:
            log = log.replace('\n', '\\n')
            self.logger.exception(log)


class Logger:

    def __init__(self,
                 username: str = 'default',
                 strategy_id: str = 'default',
                 source: str = 'trader_logger',
                 ip_address: str = '127.0.0.1',
                 debug: bool = False):
        """
        Logger는 debug모드와 production모드가 있다.
        debug 플래그를 활용하여 디버그 모드를 사용하면 DebugLogger로 스트림/파일에 로그를 남기게 된다.
        하지만 production모드로 Logger를 사용하면 TraderLogger로 로그를 남기는 LogHandler로
        메세지를 보내는 역할을 수행한다.
        """

        self.is_debug = debug

        if self.is_debug:
            self.logger = DebugLogger()
        else:
            self.logger = TraderLogger(username=username,
                                       strategy_id=strategy_id,
                                       source=source,
                                       ip_address=ip_address)

    def debug(self, log: str):
        self.logger.debug(log)

    def info(self, log: str):
        self.logger.info(log)

    def error(self, log: str):
        self.logger.error(log)

    def exception(self, log: str):
        self.logger.exception(log)


if __name__ == '__main__':
    pass
