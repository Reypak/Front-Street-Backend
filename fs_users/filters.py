import django_filters
from fs_utils.constants import IEXACT
from django.db.models import Q
from .models import CustomUser


class UserFilterSet(django_filters.FilterSet):
    is_staff = django_filters.BooleanFilter()

    class Meta:
        model = CustomUser
        fields = ['status']

    search = django_filters.CharFilter(method='advanced_filter')

    class Meta:
        abstract = True

    def advanced_filter(self, queryset, name, value):
        return queryset.filter(
            Q(phone_number__icontains=value) |
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(email__icontains=value)
        )
