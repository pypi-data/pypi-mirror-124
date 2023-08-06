import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
application = get_wsgi_application()

from db.models import OrderSuccess
from engine.events.event import Event


class TransferSuccessEvent(Event):

    def __init__(self,
                 exchange: str,
                 asset_type: str,
                 symbol: str,
                 amount: int or float,
                 **kwargs):

        self.type = 'TRANSFER_SUCCESS'
        self.exchange = exchange
        self.asset_type = asset_type
        self.symbol = symbol  # transfer시 "usdt"는 Symbol을 알 수 없음(특정 지갑으로 보내는게 아님으로), None 값
        self.amount = amount
        self.matcher = f'{exchange}_{asset_type}_{symbol}_{amount}'

    def message(self, module: str):
        pass


class RepaySuccessEvent(Event):

    def __init__(self,
                 exchange: str,
                 asset_type: str,
                 symbol: str,
                 asset: str,
                 amount: int or float,
                 **kwargs):

        self.type = 'REPAY_SUCCESS'
        self.exchange = exchange
        self.asset_type = asset_type  # usdt, margin
        self.symbol = symbol  # BTCUSDT
        self.asset = asset  # BTC
        self.amount = amount
        self.matcher = f'{exchange}_{asset_type}_{symbol}_{amount}'

    def message(self, module: str):
        pass


class LeverageSuccessEvent(Event):

    def __init__(self,
                 strategy_id: str,
                 exchange: str,
                 asset_type: str,
                 symbol: str,
                 leverage: int or float,
                 **kwargs):

        self.type = 'LEVERAGE_SUCCESS'
        self.strategy_id = strategy_id
        self.exchange = exchange
        self.asset_type = asset_type
        self.symbol = symbol
        self.leverage = leverage
        self.matcher = f'{strategy_id}_{exchange}_{asset_type}_{symbol}_{float(leverage)}'

    def message(self, module: str):
        pass


class MarginTypeSuccessEvent(Event):

    def __init__(self,
                 strategy_id: str,
                 exchange: str,
                 asset_type: str,
                 symbol: str,
                 margin_type: str,
                 **kwargs):

        self.type = 'MARGIN_TYPE_SUCCESS'
        self.strategy_id = strategy_id
        self.exchange = exchange
        self.asset_type = asset_type
        self.symbol = symbol
        self.margin_type = margin_type
        self.matcher = f'{strategy_id}_{exchange}_{asset_type}_{symbol}_{margin_type}'

    def message(self, module: str):
        pass


class OrderSuccessEvent(Event):

    def __init__(self,
                 strategy_id: str,
                 exchange: str,
                 asset_type: str,
                 symbol: str,
                 direction: str,
                 order_uid: str,
                 status: str,
                 fail_point: str = None,
                 fail_message: str = None,
                 **kwargs):

        self.type = 'ORDER_SUCCESS'
        self.strategy_id = strategy_id
        self.exchange = exchange
        self.asset_type = asset_type
        self.symbol = symbol
        self.direction = direction
        self.order_uid = order_uid
        self.status = status
        self.fail_point = fail_point
        self.fail_message = fail_message
        self.matcher = f'{exchange}_{asset_type}_{symbol}_{order_uid}'

    def message(self, module: str):
        return module

    def save(self):
        return OrderSuccess(**self.__dict__).stream_save()


class PairOrderSuccessEvent(Event):

    def __init__(self,
                 f_source,
                 f_asset_type,
                 f_symbol,
                 f_side,
                 f_direction,
                 f_order_uid,
                 s_source,
                 s_asset_type,
                 s_symbol,
                 s_side,
                 s_direction,
                 s_order_uid,
                 **kwargs):

        self.type = 'PAIR_ORDER_SUCCESS'
        self.f_source = f_source
        self.f_asset_type = f_asset_type
        self.f_symbol = f_symbol
        self.f_side = f_side
        self.f_direction = f_direction
        self.f_order_uid = f_order_uid
        self.s_source = s_source
        self.s_asset_type = s_asset_type
        self.s_symbol = s_symbol
        self.s_side = s_side
        self.s_direction = s_direction
        self.s_order_uid = s_order_uid
        self.long_matcher = None
        self.short_matcher = None
        self.matcher_maker()

    def matcher_maker(self):
        f_matcher = f'{self.f_source}_{self.f_asset_type}_{self.f_symbol}'
        s_matcher = f'{self.s_source}_{self.s_asset_type}_{self.s_symbol}'

        if self.f_direction == 'ENTRY':
            if self.f_side == 'BUY':
                self.long_matcher = f_matcher
                self.short_matcher = s_matcher
            else:
                self.long_matcher = s_matcher
                self.short_matcher = f_matcher
        elif self.f_direction == 'EXIT':
            if self.f_side == 'BUY':
                self.long_matcher = s_matcher
                self.short_matcher = f_matcher
            else:
                self.long_matcher = f_matcher
                self.short_matcher = s_matcher

    def message(self, module: str):
        pass