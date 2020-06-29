from rest_framework.exceptions import NotFound
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import HospitalCreateSerializer, HospitalRetrieveUpdateSerializer
from hospital.models import Hospital
from rest_framework.response import Response


class HospitalAPIView(ListCreateAPIView):
    serializer_class = HospitalCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Hospital.objects.all().order_by('-created_date')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class HospitalRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = HospitalRetrieveUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'pk'
    queryset = Hospital.objects.all()


# Delete Hospital with provided id
class HospitalDeleteAPIView(DestroyAPIView):
    serializer_class = HospitalRetrieveUpdateSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, *args, **kwargs):
        hospital_id = self.kwargs['pk']  # 1
        try:
            hospital = Hospital.objects.get(id=hospital_id)  # 1
            hospital.delete()
            return Response({"detail": "Hospital deleted succesfully"})
        except Hospital.DoesNotExist:
            raise NotFound("Hospital with the provided id does not exists.") #404
