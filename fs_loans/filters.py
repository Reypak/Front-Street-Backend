import django_filters
from .models import Loan
from django.db.models import Q


class BaseLoanFilterSet(django_filters.FilterSet):
    query = django_filters.CharFilter(method='advanced_filter')

    class Meta:
        abstract = True

    def advanced_filter(self, queryset, name, value):
        return queryset.filter(
            Q(borrower_name__icontains=value) |
            Q(email__icontains=value) |
            Q(phone__icontains=value) |
            Q(application_number__icontains=value)
        )
