from rest_framework import viewsets
from .serializers import *
from .models import *


class CategoryViewSet(viewsets.ModelViewSet):
    # define queryset
    queryset = Category.objects.all()

    # specify serializer to be used
    serializer_class = CategorySerializer
