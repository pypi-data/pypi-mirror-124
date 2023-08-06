from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from db.views import (
    StrategyPositionView,
    StrategyHoldingsView,

    LoginView,
    UserAPIView,
    UserDetailAPIView,
    UserProfileDetailAPIView,
    SymbolAPIView,
    SymbolDetailAPIView,
    UniverseAPIView,
    UniverseDetailAPIView,

    StrategyAPIView,
    StrategyDetailAPIView,
    CryptoHourDataAPIView,

    SignalAPIView,
    PairSignalAPIView,
    OrderAPIView,
    FillAPIView,
    OrderSuccessAPIView,
)

urlpatterns = [
    path('position/', StrategyPositionView.as_view()),
    path('holdings/', StrategyHoldingsView.as_view()),

    path('login/', LoginView.as_view()),
    path('user/', UserAPIView.as_view()),
    path('user/<int:pk>/', UserDetailAPIView.as_view()),
    path('profile/<int:pk>/', UserProfileDetailAPIView.as_view()),
    path('symbol/', SymbolAPIView.as_view()),
    path('symbol/<int:pk>/', SymbolDetailAPIView.as_view()),
    path('universe/', UniverseAPIView.as_view()),

    path('strategy/', StrategyAPIView.as_view()),

    path('crypto-hour/', CryptoHourDataAPIView.as_view()),

    path('signal/', SignalAPIView.as_view()),
    path('pair-signal/', PairSignalAPIView.as_view()),
    path('order/', OrderAPIView.as_view()),
    path('fill/', FillAPIView.as_view()),
    path('order-success/', OrderSuccessAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
