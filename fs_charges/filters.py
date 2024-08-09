import django_filters
from .models import *


class ChargeFilterSet(django_filters.FilterSet):
    type = django_filters.CharFilter()

    class Meta:
        model = Charge
        fields = ['type']


class ChargePenaltyFilterSet(django_filters.FilterSet):
    class Meta:
        model = ChargePenalty
        fields = '__all__'
