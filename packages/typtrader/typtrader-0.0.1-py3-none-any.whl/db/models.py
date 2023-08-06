from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from app.settings import PUSH_SOCKET

EXCHANGE_CHOICES = [
    ('binance', 'binance'),
    ('bybit', 'bybit'),
    ('upbit', 'upbit'),
    ('bithumb', 'bithumb'),
    ('coinbase', 'coinbase'),
    ('uniswap', 'uniswap'),
    ('pancakeswap', 'pancakeswap'),
    ('kiwoom', 'kiwoom'),
    ('ebest', 'ebest'),
    ('shinhan', 'shinhan'),
    ('robinhood', 'robinhood'),
    ('alpaca', 'alpaca'),
]

ASSET_TYPE_CHOICES = [
    ('spot', 'spot'),
    ('margin', 'margin'),
    ('usdt', 'usdt'),
    ('coinm', 'coinm'),
    ('kospi', 'kospi'),
    ('kosdaq', 'kosdaq'),
    ('kretf', 'kretf'),
    ('krfutures', 'krfutures'),
    ('stock', 'stock'),
    ('etf', 'etf'),
    ('futures', 'futures'),
]


SIGNAL_TYPE_CHOICES = [
    ('ENTRY', 'ENTRY'),
    ('EXIT', 'EXIT'),
]

ORDER_TYPE_CHOICES = [
    ('MKT', 'MARKET'),
    ('LMT', 'LIMIT'),
]


class User(AbstractUser):
    username = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    dob = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    zip = models.CharField(max_length=5, blank=True, null=True)


class Symbol(models.Model):
    exchange = models.CharField(max_length=20, choices=EXCHANGE_CHOICES, blank=True, null=True)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPE_CHOICES, blank=True, null=True)
    symbol = models.CharField(max_length=50, blank=True, null=True)
    symbol_id = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=False, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.symbol_id


class Universe(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='universe')
    name = models.CharField(max_length=100, blank=True, null=True)
    symbols = models.ManyToManyField(Symbol, blank=True, null=True)
    public = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return f'{self.owner.email} {self.name} {self.public}'


class Strategy(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owning_strategies')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='running_strategies')
    name = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    init_time = models.CharField(max_length=30, blank=True, null=True)
    active = models.BooleanField(default=False, blank=True, null=True)
    skip_missed = models.BooleanField(default=True, blank=True, null=True)
    universe = models.ForeignKey(Universe, on_delete=models.CASCADE, related_name='universe', blank=True, null=True)
    use_frames = models.CharField(max_length=100, blank=True, null=True)  # tick,second,minute,hour,day
    encrypt_key = models.CharField(max_length=250, blank=True, null=True)
    redis_host = models.CharField(max_length=250, blank=True, null=True)
    redis_port = models.CharField(max_length=250, blank=True, null=True)
    redis_password = models.CharField(max_length=250, blank=True, null=True)
    influxdb_host = models.CharField(max_length=250, blank=True, null=True)
    influxdb_token = models.CharField(max_length=250, blank=True, null=True)
    influxdb_org = models.CharField(max_length=250, blank=True, null=True)
    influxdb_bucket = models.CharField(max_length=250, blank=True, null=True)
    data_server_host = models.CharField(max_length=250, blank=True, null=True)
    data_server_port = models.CharField(max_length=250, blank=True, null=True)
    data_proxy_host = models.CharField(max_length=250, blank=True, null=True)
    data_proxy_market_port = models.CharField(max_length=250, blank=True, null=True)
    data_proxy_account_port = models.CharField(max_length=250, blank=True, null=True)
    data_proxy_bar_port = models.CharField(max_length=250, blank=True, null=True)
    strategy_queue_host = models.CharField(max_length=250, blank=True, null=True)
    strategy_queue_port = models.CharField(max_length=250, blank=True, null=True)
    order_queue_host = models.CharField(max_length=250, blank=True, null=True)
    order_queue_port = models.CharField(max_length=250, blank=True, null=True)
    execution_queue_host = models.CharField(max_length=250, blank=True, null=True)
    execution_queue_port = models.CharField(max_length=250, blank=True, null=True)
    binance_public_key = models.CharField(max_length=250, blank=True, null=True)
    binance_private_key = models.CharField(max_length=250, blank=True, null=True)
    bybit_public_key = models.CharField(max_length=250, blank=True, null=True)
    bybit_private_key = models.CharField(max_length=250, blank=True, null=True)
    upbit_public_key = models.CharField(max_length=250, blank=True, null=True)
    upbit_private_key = models.CharField(max_length=250, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.email} {self.name} {self.active}'


class Log(models.Model):
    username = models.CharField(max_length=200, blank=True, null=True)
    strategy_id = models.CharField(max_length=200, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    ip_address = models.CharField(max_length=30, blank=True, null=True)
    log_level = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.username} {self.strategy_id} {self.created} {self.source} {self.log_level} {self.message}'

    def update(self, **kwargs):
        mfields = iter(self._meta.fields)
        mods = [(f.attname, kwargs[f.attname]) for f in mfields if f.attname in kwargs]
        for fname, fval in mods:
            setattr(self, fname, fval)
        super().save()

    def stream_save(self):
        self.save()
        inst_dict = self.__dict__.copy()
        _ = inst_dict.pop('_state')
        _ = inst_dict.pop('updated')
        inst_dict['created'] = inst_dict['created'].strftime('%Y-%m-%d %H:%M:%S.%f')
        model_name = self._meta.object_name.upper()
        evt = {'event': f'{model_name}_CREATED', 'data': inst_dict}
        PUSH_SOCKET.publish(evt)

    def stream_update(self, **kwargs):
        self.update(**kwargs)
        inst_dict = self.__dict__.copy()
        _ = inst_dict.pop('_state')
        model_name = self._meta.object_name.upper()
        evt = {'event': f'{model_name}_UPDATED', 'data': inst_dict}
        PUSH_SOCKET.publish(evt)


class CryptoMinuteData(models.Model):
    exchange = models.CharField(max_length=20, choices=EXCHANGE_CHOICES, blank=True, null=True)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPE_CHOICES, blank=True, null=True)
    symbol = models.CharField(max_length=50, blank=True, null=True)
    symbol_id = models.CharField(max_length=100, blank=True, null=True)
    date = models.CharField(max_length=14, blank=True, null=True)  # yyyymmddHHMMSS
    open_prc = models.FloatField(blank=True, null=True)
    high_prc = models.FloatField(blank=True, null=True)
    low_prc = models.FloatField(blank=True, null=True)
    close_prc = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'{self.symbol_id} {self.date}'


class CryptoHourData(models.Model):
    exchange = models.CharField(max_length=20, choices=EXCHANGE_CHOICES, blank=True, null=True)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPE_CHOICES, blank=True, null=True)
    symbol = models.CharField(max_length=50, blank=True, null=True)
    symbol_id = models.CharField(max_length=100, blank=True, null=True)
    date = models.CharField(max_length=14, blank=True, null=True)  # yyyymmddHHMMSS
    open_prc = models.FloatField(blank=True, null=True)
    high_prc = models.FloatField(blank=True, null=True)
    low_prc = models.FloatField(blank=True, null=True)
    close_prc = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f'{self.symbol_id} {self.date}'


# Ledger 관련 모델
class Signal(models.Model):
    username = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(max_length=30, blank=True, null=True)
    strategy_id = models.CharField(max_length=200, blank=True, null=True)  # Strategy name
    exchange = models.CharField(max_length=20, choices=EXCHANGE_CHOICES, blank=True, null=True)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPE_CHOICES, blank=True, null=True)
    symbol = models.CharField(max_length=50, blank=True, null=True)
    signal_type = models.CharField(max_length=5, choices=SIGNAL_TYPE_CHOICES, blank=True, null=True)
    signal_price = models.FloatField(blank=True, null=True)
    order_type = models.CharField(max_length=3, choices=ORDER_TYPE_CHOICES, blank=True, null=True)
    log_time = models.CharField(max_length=30, blank=True, null=True)
    signal_uid = models.CharField(max_length=50, blank=True, null=True)  # SHA1

    def __str__(self):
        return f'{self.log_time} {self.strategy_id} {self.exchange} {self.asset_type} {self.symbol} {self.signal_type} {self.order_type} {self.signal_price}'

    def update(self, **kwargs):
        mfields = iter(self._meta.fields)
        mods = [(f.attname, kwargs[f.attname]) for f in mfields if f.attname in kwargs]
        for fname, fval in mods:
            setattr(self, fname, fval)
        super().save()

    def stream_save(self):
        self.save()
        inst_dict = self.__dict__.copy()
        _ = inst_dict.pop('_state')
        model_name = self._meta.object_name.upper()
        evt = {'event': f'{model_name}_CREATED', 'data': inst_dict}
        PUSH_SOCKET.publish(evt)

    def stream_update(self, **kwargs):
        self.update(**kwargs)
        inst_dict = self.__dict__.copy()
        _ = inst_dict.pop('_state')
        model_name = self._meta.object_name.upper()
        evt = {'event': f'{model_name}_UPDATED', 'data': inst_dict}
        PUSH_SOCKET.publish(evt)


class PairSignal(models.Model):
    username = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(max_length=30, blank=True, null=True)
    strategy_id = models.CharField(max_length=200, blank=True, null=True)
    long_info = models.CharField(max_length=150, blank=True, null=True)
    short_info = models.CharField(max_length=150, blank=True, null=True)
    signal_type = models.CharField(max_length=5, choices=SIGNAL_TYPE_CHOICES, blank=True, null=True)
    long_cur_price = models.FloatField(blank=True, null=True)
    short_cur_price = models.FloatField(blank=True, null=True)
    order_type = models.CharField(max_length=3, choices=ORDER_TYPE_CHOICES, blank=True, null=True)
    log_time = models.CharField(max_length=30, blank=True, null=True)
    signal_uid = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.log_time} {self.strategy_id} LONG: {self.long_info} {self.long_cur_price} | SHORT: {self.short_info} {self.short_cur_price}'

    def update(self, **kwargs):
        mfields = iter(self._meta.fields)
        mods = [(f.attname, kwargs[f.attname]) for f in mfields if f.attname in kwargs]
        for fname, fval in mods:
            setattr(self, fname, fval)
        super().save()

    def stream_save(self):
        self.save()
        inst_dict = self.__dict__.copy()
        _ = inst_dict.pop('_state')
        model_name = self._meta.object_name.upper()
        evt = {'event': f'{model_name}_CREATED', 'data': inst_dict}
        PUSH_SOCKET.publish(evt)

    def stream_update(self, **kwargs):
        self.update(**kwargs)
        inst_dict = self.__dict__.copy()
        _ = inst_dict.pop('_state')
        model_name = self._meta.object_name.upper()
        evt = {'event': f'{model_name}_UPDATED', 'data': inst_dict}
        PUSH_SOCKET.publish(evt)


class Order(models.Model):
    username = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(max_length=150, blank=True, null=True)
    strategy_id = models.CharField(max_length=150, blank=True, null=True)
    exchange = models.CharField(max_length=150, blank=True, null=True)  # binance, bybit
    asset_type = models.CharField(max_length=150, blank=True, null=True)  # usdt, coinm, spot, margin
    symbol = models.CharField(max_length=150, blank=True, null=True)
    order_type = models.CharField(max_length=150, blank=True, null=True)  # MKT, LMT
    quantity = models.FloatField(max_length=150, blank=True, null=True)
    price = models.FloatField(max_length=150, blank=True, null=True)
    side = models.CharField(max_length=150, blank=True, null=True)  # BUY, SELL
    direction = models.CharField(max_length=150, blank=True, null=True)  # ENTRY, EXIT
    leverage_size = models.FloatField(max_length=150, blank=True, null=True)
    margin_type = models.CharField(max_length=150, blank=True, null=True)
    invest_amount = models.FloatField(max_length=150, blank=True, null=True)
    signal_uid = models.CharField(max_length=150, blank=True, null=True)
    paired = models.CharField(max_length=10, blank=True, null=True)
    est_fill_cost = models.FloatField(max_length=150, blank=True, null=True)
    matcher = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(max_length=150, blank=True, null=True)  # Exec 에서 바로 status 수정하기도하고 SuccessEvent 받고 수정하기도하고 -> Exec는 루프둘면서 Status 별 행동 취해주면됨!
    api_order_uid = models.CharField(max_length=150, blank=True, null=True)
    remaining_quantity = models.FloatField(max_length=150, blank=True, null=True)
    log_time = models.CharField(max_length=150, blank=True, null=True)
    order_uid = models.CharField(max_length=150, blank=True, null=True)

    leverage_confirmed = models.CharField(max_length=10, blank=True, null=True) # True, False
    margin_type_confirmed = models.CharField(max_length=10, blank=True, null=True) # True, False
    transfer_confirmed = models.CharField(max_length=10, blank=True, null=True) # True, False
    order_confirmed = models.CharField(max_length=10, blank=True, null=True) # True, False
    repay_confirmed = models.CharField(max_length=10, blank=True, null=True) # True, False

    repay_needed = models.CharField(max_length=10, blank=True, null=True)

    order_status = models.BooleanField(blank=True, null=True)
    order_fail_point = models.CharField(max_length=20, blank=True, null=True)
    fail_message = models.CharField(max_length=300, blank=True, null=True)

    retry = models.BooleanField(blank=True, null=True)
    retry_num = models.IntegerField(blank=True, null=True)
    retry_cnt = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.exchange}_{self.asset_type}_{self.symbol}_{self.side}_{self.quantity}'

    def update(self, **kwargs):
        mfields = iter(self._meta.fields)
        mods = [(f.attname, kwargs[f.attname]) for f in mfields if f.attname in kwargs]
        for fname, fval in mods:
            setattr(self, fname, fval)
        super().save()

    def stream_save(self):
        self.save()
        inst_dict = self.__dict__.copy()
        _ = inst_dict.pop('_state')
        model_name = self._meta.object_name.upper()
        evt = {'event': f'{model_name}_CREATED', 'data': inst_dict}
        PUSH_SOCKET.publish(evt)

    def stream_update(self, **kwargs):
        self.update(**kwargs)
        inst_dict = self.__dict__.copy()
        _ = inst_dict.pop('_state')
        model_name = self._meta.object_name.upper()
        evt = {'event': f'{model_name}_UPDATED', 'data': inst_dict}
        PUSH_SOCKET.publish(evt)


class Fill(models.Model):
    username = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(max_length=150, blank=True, null=True)
    strategy_id = models.CharField(max_length=150, blank=True, null=True)  # TODO :: Not used yet
    exchange = models.CharField(max_length=150, blank=True, null=True)  # binance, bybit
    asset_type = models.CharField(max_length=150, blank=True, null=True)  # usdt, coinm, spot, margin
    symbol = models.CharField(max_length=150, blank=True, null=True)
    side = models.CharField(max_length=150, blank=True, null=True)  # BUY, SELL
    direction = models.CharField(max_length=150, blank=True, null=True)  # Order 매칭될때 받아오기!
    filled_quantity = models.FloatField(max_length=150, blank=True, null=True)
    order_quantity = models.FloatField(max_length=150, blank=True, null=True)
    fill_cost = models.FloatField(max_length=150, blank=True, null=True)
    est_fill_cost = models.FloatField(max_length=150, blank=True, null=True)
    api_order_uid = models.CharField(max_length=150, blank=True, null=True)
    matcher = models.CharField(max_length=150, blank=True, null=True)
    order_uid = models.CharField(max_length=150, blank=True, null=True)
    signal_uid = models.CharField(max_length=150, blank=True, null=True)  # Order 매칭될때 받아오기!
    accno = models.CharField(max_length=150, blank=True, null=True)  # TODO :: Not used yet
    log_time = models.CharField(max_length=150, blank=True, null=True)
    commission = models.FloatField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f'{self.exchange}_{self.asset_type}_{self.symbol}_{self.side}_{self.order_quantity}_{self.filled_quantity}'

    def update(self, **kwargs):
        mfields = iter(self._meta.fields)
        mods = [(f.attname, kwargs[f.attname]) for f in mfields if f.attname in kwargs]
        for fname, fval in mods:
            setattr(self, fname, fval)
        super().save()

    def stream_save(self):
        self.save()
        inst_dict = self.__dict__.copy()
        _ = inst_dict.pop('_state')
        model_name = self._meta.object_name.upper()
        evt = {'event': f'{model_name}_CREATED', 'data': inst_dict}
        PUSH_SOCKET.publish(evt)

    def stream_update(self, **kwargs):
        self.update(**kwargs)
        inst_dict = self.__dict__.copy()
        _ = inst_dict.pop('_state')
        model_name = self._meta.object_name.upper()
        evt = {'event': f'{model_name}_UPDATED', 'data': inst_dict}
        PUSH_SOCKET.publish(evt)


class OrderSuccess(models.Model):
    username = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(max_length=150, blank=True, null=True)
    strategy_id = models.CharField(max_length=150, blank=True, null=True)
    exchange = models.CharField(max_length=150, blank=True, null=True)  # binance, bybit
    asset_type = models.CharField(max_length=150, blank=True, null=True)  # usdt, coinm, spot, margin
    symbol = models.CharField(max_length=150, blank=True, null=True)
    direction = models.CharField(max_length=150, blank=True, null=True)
    order_uid = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(max_length=150, blank=True, null=True)
    fail_point = models.CharField(max_length=150, blank=True, null=True)
    fail_message = models.CharField(max_length=150, blank=True, null=True)
    matcher = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f'{self.strategy_id}_{self.exchange}_{self.asset_type}_{self.symbol}_{self.order_uid}'

    def update(self, **kwargs):
        mfields = iter(self._meta.fields)
        mods = [(f.attname, kwargs[f.attname]) for f in mfields if f.attname in kwargs]
        for fname, fval in mods:
            setattr(self, fname, fval)
        super().save()

    def stream_save(self):
        self.save()
        inst_dict = self.__dict__.copy()
        _ = inst_dict.pop('_state')
        model_name = self._meta.object_name.upper()
        evt = {'event': f'{model_name}_CREATED', 'data': inst_dict}
        PUSH_SOCKET.publish(evt)

    def stream_update(self, **kwargs):
        self.update(**kwargs)
        inst_dict = self.__dict__.copy()
        _ = inst_dict.pop('_state')
        model_name = self._meta.object_name.upper()
        evt = {'event': f'{model_name}_UPDATED', 'data': inst_dict}
        PUSH_SOCKET.publish(evt)