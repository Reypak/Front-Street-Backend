from rest_framework import viewsets

from utils.filters.filter_backends import DEFAULT_FILTER_BACKENDS
from utils.filters.filters import LoanReportFilterSet
from .serializers import LoanReportSerializer
from .models import LoanReport

# Create your views here.


class LoanReportViewSet(viewsets.ModelViewSet):
    queryset = LoanReport.objects.all()
    serializer_class = LoanReportSerializer
    filter_backends = DEFAULT_FILTER_BACKENDS
    filterset_class = LoanReportFilterSet
