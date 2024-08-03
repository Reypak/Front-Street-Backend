import django_filters
from fs_utils.constants import ICONTAINS
from .models import *


class TransactionFilterSet(django_filters.FilterSet):
    ref_number = django_filters.CharFilter(
        lookup_expr=ICONTAINS,  field_name="loan__ref_number")
    client_name = django_filters.CharFilter(
        field_name="loan__client.display_name", lookup_expr=ICONTAINS)

    class Meta:
        model = Transaction
        fields = ['client_name', 'ref_number']
