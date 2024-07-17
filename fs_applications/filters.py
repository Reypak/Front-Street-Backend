import django_filters

from fs_utils.constants import IEXACT
from .models import Application
from django.db.models import Q


class BaseApplicationFilterSet(django_filters.FilterSet):
    search = django_filters.CharFilter(method='advanced_filter')

    class Meta:
        abstract = True

    def advanced_filter(self, queryset, name, value):
        return queryset.filter(
            Q(ref_number__icontains=value) |
            Q(client__first_name__icontains=value) |
            Q(client__last_name__icontains=value) |
            Q(client__email__icontains=value) |
            Q(client__phone_number__icontains=value) |
            Q(loan__ref_number__icontains=value)
        )


class ApplicationFilterSet(BaseApplicationFilterSet):
    status = django_filters.CharFilter(
        lookup_expr=IEXACT,)
    client = django_filters.CharFilter()

    # application_number = django_filters.CharFilter(
    #     lookup_expr=IEXACT,  field_name="loan__application_number")

    class Meta:
        model = Application
        fields = [
            'client',
            'status'
        ]
