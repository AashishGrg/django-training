from django.urls import path
from .views import SignupAPIView, LoginAPIView

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='user_register'),
    path('login/', LoginAPIView.as_view(), name='login_api'),
]
