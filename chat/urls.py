# chat/urls.py
from django.urls import path
from .views import RegisterAPIView, LoginAPIView, ProfileAPIView, MessageAPIView,UserView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('messages/', MessageAPIView.as_view(), name='messages'),
    path('user/', UserView.as_view()),
]
