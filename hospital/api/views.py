from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import HospitalCreateSerializer
from hospital.models import Hospital


class HospitalAPIView(ListCreateAPIView):
    serializer_class = HospitalCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Hospital.objects.all().order_by('-created_date')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
