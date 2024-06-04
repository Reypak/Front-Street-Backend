from rest_framework import viewsets
from .serializers import LoanTypeSerializer
from .models import LoanType

# Create your views here.

# create a viewset


class LoanTypeViewSet(viewsets.ModelViewSet):
    # define queryset
    queryset = LoanType.objects.all()

    # specify serializer to be used
    serializer_class = LoanTypeSerializer
