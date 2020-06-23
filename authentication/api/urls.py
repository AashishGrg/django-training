from django.urls import path
from .views import SignupAPIView, LoginAPIView, PasswordChangeAPIView

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='user_register'),
    path('login/', LoginAPIView.as_view(), name='login_api'),
    path('password/change/', PasswordChangeAPIView.as_view(), name='password_change_api'),
]
