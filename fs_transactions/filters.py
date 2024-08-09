import django_filters
from fs_utils.constants import ICONTAINS
from .models import *
from django.db.models import Q


class TransactionFilterSet(django_filters.FilterSet):
    ref_number = django_filters.CharFilter(
        lookup_expr=ICONTAINS,  field_name="loan__ref_number")
    client_name = django_filters.CharFilter(
        method="advanced_filter", lookup_expr=ICONTAINS)
    type = django_filters.CharFilter()

    class Meta:
        model = Transaction
        fields = ['client_name', 'ref_number', 'type']

    def advanced_filter(self, queryset, name, value):
        return queryset.filter(
            Q(loan__client__first_name__icontains=value) |
            Q(loan__client__last_name__icontains=value)
        )
