from django.urls import path
from .views import HospitalAPIView

urlpatterns = [
    path('create/', HospitalAPIView.as_view(), name='hospital_create'),
    path('list/', HospitalAPIView.as_view(), name='hospital_list'),
]
