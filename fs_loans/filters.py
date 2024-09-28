import django_filters

from fs_utils.constants import ICONTAINS, IEXACT
from .models import Loan
from django.db.models import Q


class BaseLoanFilterSet(django_filters.FilterSet):
    search = django_filters.CharFilter(method='advanced_filter')

    class Meta:
        abstract = True

    def advanced_filter(self, queryset, name, value):
        return queryset.filter(
            Q(ref_number__icontains=value) |
            Q(client__first_name__icontains=value) |
            Q(client__last_name__icontains=value) |
            Q(client__email__icontains=value) |
            Q(client__phone_number__icontains=value)
        )


class LoanFilterSet(BaseLoanFilterSet):
    ref_number = django_filters.CharFilter(lookup_expr=IEXACT)
    status = django_filters.CharFilter(lookup_expr=IEXACT)
    # client = django_filters.CharFilter(
    #     field_name="client__first_name", lookup_expr=ICONTAINS)
    category = django_filters.CharFilter(lookup_expr=IEXACT)
    client = django_filters.CharFilter()
    # field name
    category_name = django_filters.CharFilter(
        field_name="category__name", lookup_expr=ICONTAINS)
    is_overdue = django_filters.BooleanFilter()

    class Meta:
        model = Loan
        fields = ['client',
                  'status',
                  'category',
                  'category_name',
                  'is_overdue',
                  'is_due_today',
                  'ref_number']
