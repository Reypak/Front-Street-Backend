import django_filters

from fs_utils.constants import ICONTAINS, IEXACT
from .models import *


class CommentFilterSet(django_filters.FilterSet):
    object_id = django_filters.NumberFilter(field_name='object_id')
    type = django_filters.CharFilter(
        field_name="content_type__model")

    class Meta:
        model = Comment
        fields = ['object_id', 'type']
