from rest_framework import viewsets

from fs_utils.filters.filter_backends import DEFAULT_FILTER_BACKENDS
from fs_utils.filters.filters import LoanPaymentFilterSet
from .serializers import LoanPaymentSerializer
from .models import LoanPayment
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

# Create your views here.


class LoanPaymentViewSet(viewsets.ModelViewSet):
    queryset = LoanPayment.objects.all()
    serializer_class = LoanPaymentSerializer
    filter_backends = DEFAULT_FILTER_BACKENDS
    filterset_class = LoanPaymentFilterSet
    permission_classes = [IsAuthenticated]


class LoanPaymentsList(generics.ListAPIView):
    serializer_class = LoanPaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        loan_id = self.kwargs['loan_id']
        return LoanPayment.objects.filter(loan=loan_id)
