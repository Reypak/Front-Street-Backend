import django_filters
from .models import *


class InstallmentFilterSet(django_filters.FilterSet):
    # loan = django_filters.CharFilter()
    due_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Installment
        fields = '__all__'
