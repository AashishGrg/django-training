from django.urls import path
from .views import HospitalAPIView, HospitalRetrieveUpdateAPIView,HospitalDeleteAPIView

urlpatterns = [
    path('create/', HospitalAPIView.as_view(), name='hospital_create'),
    path('list/', HospitalAPIView.as_view(), name='hospital_list'),
    path('<int:pk>/', HospitalRetrieveUpdateAPIView.as_view(), name='hospital_detail_update'),
    path('delete/<int:pk>/', HospitalDeleteAPIView.as_view(), name='hospital_delete'),
]
