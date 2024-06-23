import django_filters

from fs_utils.constants import ICONTAINS
from .models import *


class ClientFilterSet(django_filters.FilterSet):

    first_name = django_filters.CharFilter(lookup_expr=ICONTAINS)
    last_name = django_filters.CharFilter(lookup_expr=ICONTAINS)
    email = django_filters.CharFilter(lookup_expr=ICONTAINS)

    class Meta:
        model = Client
        fields = [
            'email',
            'first_name',
            'last_name',
        ]
