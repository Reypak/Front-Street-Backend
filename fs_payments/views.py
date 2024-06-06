from rest_framework import viewsets

from fs_utils.filters.filter_backends import DEFAULT_FILTER_BACKENDS
from fs_utils.filters.filters import LoanPaymentFilterSet
from .serializers import LoanPaymentSerializer
from .models import LoanPayment

# Create your views here.


class LoanPaymentViewSet(viewsets.ModelViewSet):
    queryset = LoanPayment.objects.all()
    serializer_class = LoanPaymentSerializer
    filter_backends = DEFAULT_FILTER_BACKENDS
    filterset_class = LoanPaymentFilterSet
