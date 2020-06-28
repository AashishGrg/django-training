from rest_framework import serializers
from hospital.models import Hospital


class HospitalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ('id', 'created_by', 'name', 'latitude', 'longitude', 'address', 'description', 'image', 'is_active')
        read_only_fields = ('id', 'created_by', 'is_active',)
