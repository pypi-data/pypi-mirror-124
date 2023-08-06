import redis
from flatten_dict import unflatten
from django.contrib.auth.hashers import check_password

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter, OrderingFilter

from app.settings import (
    PUSH_SOCKET,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PW,
)
from db.permissions import (
    UserAPIPermission,
    UserDetailAPIPermission,
    UserProfileDetailAPIPermission,
    SymbolAPIPermission,
)
from db.paginations import (
    StandardResultPagination,
    BulkResultPagination,
)
from db.models import (
    User,
    UserProfile,
    Symbol,
    Universe,
    Strategy,
    CryptoHourData,
    Signal,
    PairSignal,
    Order,
    Fill,
    OrderSuccess,
)
from db.serializers import (
    UserSerializer,
    UserProfileSerializer,
    SymbolSerializer,
    UniverseSerializer,
    StrategySerializer,
    CryptoHourDataSerializer,
    SignalSerializer,
    PairSignalSerializer,
    OrderSerializer,
    FillSerializer,
    OrderSuccessSerializer,
)

redis_conn = redis.StrictRedis(host=REDIS_HOST,
                               port=REDIS_PORT,
                               password=REDIS_PW)


class StrategyPositionView(APIView):
    def post(self, request):
        strategy_id = request.data.get('strategy_id')
        if strategy_id is not None:
            pos_key = f'position_{strategy_id}'
            res = redis_conn.hgetall(pos_key)
            res = {key.decode('utf-8'): float(val.decode('utf-8')) for key, val in res.items()}
            unflatten_res = unflatten(res, splitter='underscore')
            return Response({'status': 'SUCCESS', 'data': unflatten_res})
        else:
            return Response({'status': 'FAIL', 'detail': 'no such strategy_id'})


class StrategyHoldingsView(APIView):
    def post(self, request):
        strategy_id = request.data.get('strategy_id')
        if strategy_id is not None:
            hold_key = f'holdings_{strategy_id}'
            res = redis_conn.hgetall(hold_key)
            res = {key.decode('utf-8'): float(val.decode('utf-8')) for key, val in res.items()}
            unflatten_res = unflatten(res, splitter='underscore')
            return Response({'status': 'SUCCESS', 'data': unflatten_res})
        else:
            return Response({'status': 'FAIL', 'detail': 'no such strategy_id'})


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(email=username).first()
        if user is not None:
            auth = check_password(password, user.password)
            if auth:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'status': 'SUCCESS', 'Token': token.key, 'id': user.id})
            else:
                return Response({'status': 'FAIL', 'detail': 'wrong login credentials'})
        else:
            return Response({'status': 'FAIL', 'detail': 'wrong login credentials'})


# [User + UserProfile]
class UserAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserAPIPermission]
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]


class UserStreamAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserAPIPermission]
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def post(self, request, *args, **kwargs):
        created = self.create(request, *args, **kwargs)
        evt = {
            'event': 'USER_CREATED',
            'data': created.data
        }
        PUSH_SOCKET.publish(evt)
        return created


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserDetailAPIPermission]


"""
TODO:: 유저 업데이트/삭제/수정되는 정보를 소켓으로 스트리밍하기
"""
# class UserDetailStreamAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [UserDetailAPIPermission]


class UserProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [UserProfileDetailAPIPermission]

    def get_object(self):
        """
        user, profile id값이 다르기 때문에 request obj는 user id로 필터링하여 불러오기
        """
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        queryset = User.objects.all()
        obj = generics.get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj.profile


# [Symbol]
class SymbolAPIView(generics.ListCreateAPIView):
    queryset = Symbol.objects.all()
    serializer_class = SymbolSerializer
    permission_classes = [SymbolAPIPermission]
    pagination_class = BulkResultPagination
    filter_backends = [SearchFilter, OrderingFilter]


class SymbolStreamAPIView(generics.ListCreateAPIView):
    queryset = Symbol.objects.all()
    serializer_class = SymbolSerializer
    permission_classes = [SymbolAPIPermission]
    pagination_class = BulkResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def post(self, request, *args, **kwargs):
        created = self.create(request, *args, **kwargs)
        evt = {
            'event': 'SYMBOL_CREATED',
            'data': created.data
        }
        PUSH_SOCKET.publish(evt)
        return created


class SymbolDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Symbol.objects.all()
    serializer_class = SymbolSerializer
    permission_classes = [permissions.IsAdminUser]


# [Universe]
class UniverseAPIView(generics.ListCreateAPIView):
    queryset = Universe.objects.all()
    serializer_class = UniverseSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def create(self, request, *args, **kwargs):
        """
        symbols는 ManyToManyField이기 때문에 symbol만 따로 pop시켜서
        universe를 생성한 다음 add해준다.
        """
        symbols = request.data.getlist('symbols')
        symbols = [int(sym_id) for sym_id in symbols]
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        new_id = serializer.data['id']
        universe = Universe.objects.get(id=new_id)
        for sym_id in symbols:
            universe.symbols.add(sym_id)
        headers = self.get_success_headers(serializer.data)
        return_data = {
            **serializer.data,
            'symbols': list(universe.symbols.values('id', 'symbol_id'))
        }
        return Response(return_data, status=status.HTTP_201_CREATED, headers=headers)


class UniverseStreamAPIView(generics.ListCreateAPIView):
    queryset = Universe.objects.all()
    serializer_class = UniverseSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def create(self, request, *args, **kwargs):
        symbols = request.data.getlist('symbols')
        symbols = [int(sym_id) for sym_id in symbols]
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        new_id = serializer.data['id']
        universe = Universe.objects.get(id=new_id)
        for sym_id in symbols:
            universe.symbols.add(sym_id)
        headers = self.get_success_headers(serializer.data)
        return_data = {
            **serializer.data,
            'symbols': list(universe.symbols.values('id', 'symbol_id'))
        }
        return Response(return_data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        created = self.create(request, *args, **kwargs)
        evt = {
            'event': 'UNIVERSE_CREATED',
            'data': created.data
        }
        PUSH_SOCKET.publish(evt)
        return created


class UniverseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    pass


# [Strategy]
class StrategyAPIView(generics.ListCreateAPIView):
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]


class StrategyStreamAPIView(generics.ListCreateAPIView):
    pass


class StrategyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    pass


# [CryptoHourData]
class CryptoHourDataAPIView(generics.ListAPIView):
    queryset = CryptoHourData.objects.all()
    serializer_class = CryptoHourDataSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = BulkResultPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['symbol_id']


# [Signal]
class SignalAPIView(generics.ListCreateAPIView):
    queryset = Signal.objects.all()
    serializer_class = SignalSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['strategy_id']

    def get_queryset(self, *args, **kwargs):
        queryset = Signal.objects.all()
        filter_fields = ['username', 'strategy_id', 'exchange',
                         'asset_type', 'symbol', 'signal_type']
        filters = {field: self.request.GET.get(field) for field in filter_fields}
        filters = {field: value for field, value in filters.items() if value is not None}
        queryset = queryset.filter(**filters)
        return queryset


# [PairSignal]
class PairSignalAPIView(generics.ListCreateAPIView):
    queryset = PairSignal.objects.all()
    serializer_class = SignalSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['strategy_id']

    def get_queryset(self, *args, **kwargs):
        queryset = PairSignal.objects.all()
        filter_fields = ['username', 'strategy_id', 'signal_type']
        filters = {field: self.request.GET.get(field) for field in filter_fields}
        filters = {field: value for field, value in filters.items() if value is not None}
        queryset = queryset.filter(**filters)
        return queryset


# [Order]
class OrderAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['strategy_id']

    def get_queryset(self, *args, **kwargs):
        queryset = Order.objects.all()
        filter_fields = ['username', 'strategy_id', 'exchange',
                         'asset_type', 'symbol', 'side', 'direction']
        filters = {field: self.request.GET.get(field) for field in filter_fields}
        filters = {field: value for field, value in filters.items() if value is not None}
        queryset = queryset.filter(**filters)
        return queryset


# [Fill]
class FillAPIView(generics.ListCreateAPIView):
    queryset = Fill.objects.all()
    serializer_class = FillSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['strategy_id']

    def get_queryset(self, *args, **kwargs):
        queryset = Fill.objects.all()
        filter_fields = ['username', 'strategy_id', 'exchange',
                         'asset_type', 'symbol', 'side', 'direction']
        filters = {field: self.request.GET.get(field) for field in filter_fields}
        filters = {field: value for field, value in filters.items() if value is not None}
        queryset = queryset.filter(**filters)
        return queryset


# [OrderSuccess]
class OrderSuccessAPIView(generics.ListCreateAPIView):
    queryset = OrderSuccess.objects.all()
    serializer_class = OrderSuccessSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['strategy_id']

    def get_queryset(self, *args, **kwargs):
        queryset = OrderSuccess.objects.all()
        filter_fields = ['username', 'strategy_id', 'exchange',
                         'asset_type', 'symbol', 'direction']
        filters = {field: self.request.GET.get(field) for field in filter_fields}
        filters = {field: value for field, value in filters.items() if value is not None}
        queryset = queryset.filter(**filters)
        return queryset
