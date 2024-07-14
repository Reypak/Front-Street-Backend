from rest_framework import viewsets

from fs_categories.filters import CategoryFilterSet
from fs_utils.filters.filter_backends import DEFAULT_FILTER_BACKENDS
from .serializers import *
from .models import *


class CategoryViewSet(viewsets.ModelViewSet):
    # define queryset
    queryset = Category.objects.all()

    filter_backends = DEFAULT_FILTER_BACKENDS
    filterset_class = CategoryFilterSet

    # specify serializer to be used
    serializer_class = CategorySerializer
