from rest_framework import viewsets
from fs_utils.filters.filter_backends import DEFAULT_FILTER_BACKENDS
from fs_utils.filters.filters import LoanFilterSet
# from utils.constants import CustomPagination

# Create your views here.
# import local data
from .serializers import *
from .models import Loan
from rest_framework.permissions import IsAuthenticated

# create a viewset


class LoanViewSet(viewsets.ModelViewSet):
    # define queryset
    queryset = Loan.objects.all()
    permission_classes = [IsAuthenticated]

    # specify serializer to be used
    # serializer_class = LoanSerializer

    # set data filters
    filter_backends = DEFAULT_FILTER_BACKENDS
    filterset_class = LoanFilterSet

    def get_serializer_class(self):
        if self.action == 'list':
            return LoanListSerializer

        return LoanSerializer

    # for custom pagination
    # pagination_class = CustomPagination

    # def perform_create(self, serializer):
    #     return serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        return serializer.save(updated_by=self.request.user)
