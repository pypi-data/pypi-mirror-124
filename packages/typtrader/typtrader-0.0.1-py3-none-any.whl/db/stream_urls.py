from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from db.views import (
    LoginView,
    UserStreamAPIView,
    UserDetailAPIView,
    UserProfileDetailAPIView,
    SymbolStreamAPIView,
    SymbolDetailAPIView,
)

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('user/', UserStreamAPIView.as_view()),
    path('user/<int:pk>/', UserDetailAPIView.as_view()),
    path('profile/<int:pk>/', UserProfileDetailAPIView.as_view()),
    path('symbol/', SymbolStreamAPIView.as_view()),
    path('symbol/<int:pk>/', SymbolDetailAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)