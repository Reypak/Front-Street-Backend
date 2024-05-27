from rest_framework import viewsets
from .serializers import CategorySerializer
from .models import Category

# Create your views here.

# create a viewset


class CategoryViewSet(viewsets.ModelViewSet):
    # define queryset
    queryset = Category.objects.all()

    # specify serializer to be used
    serializer_class = CategorySerializer
