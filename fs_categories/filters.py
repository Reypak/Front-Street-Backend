import django_filters

from fs_categories.models import Category


class CategoryFilterSet(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = Category
        fields = ['is_active']
