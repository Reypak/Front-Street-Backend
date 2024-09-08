import django_filters
from .models import *


class TaskFilterSet(django_filters.FilterSet):
    status = django_filters.CharFilter()
    object_id = django_filters.NumberFilter(field_name='object_id')
    type = django_filters.CharFilter(
        field_name="content_type__model")
    assignee = django_filters.ModelMultipleChoiceFilter(
        field_name='assignees',
        queryset=CustomUser.objects.all(),
        to_field_name='id',  # Filtering based on User ID
        label='Assignee'
    )
