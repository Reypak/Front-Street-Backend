import django_filters

from fs_utils.constants import IEXACT
from .models import Application


class ApplicationFilterSet(django_filters.FilterSet):
    # application_number = django_filters.CharFilter(
    #     lookup_expr=IEXACT,  field_name="loan__application_number")

    class Meta:
        model = Application
        fields = [
            # 'application_number'
        ]
