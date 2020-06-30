import django_filters
from hospital.models import Hospital


class HospitalFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Hospital
        fields = ('is_active','name',)
