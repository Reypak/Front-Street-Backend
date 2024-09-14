from rest_framework import viewsets
from fs_loans.filters import LoanFilterSet
from fs_loans.permissions import LoanPermission

# from utils.constants import CustomPagination

# Create your views here.
# import local data
from .serializers import *
from .models import Loan
# from rest_framework.permissions import IsAuthenticated

# create a viewset


class LoanViewSet(viewsets.ModelViewSet):
    # define queryset
    queryset = Loan.objects.all()
    permission_classes = [LoanPermission]

    # specify serializer to be used
    # serializer_class = LoanSerializer

    # set data filters
    filterset_class = LoanFilterSet

    def get_queryset(self):
        user = self.request.user
        if user.is_staff is True:
            # show all for staff
            queryset = Loan.objects.all()
        else:
            # only for user
            queryset = Loan.objects.filter(client=user)
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return LoanListSerializer
        if self.action == 'retrieve':
            return LoanViewSerializer

        return LoanSerializer

    # for custom pagination
    # pagination_class = CustomPagination

    # def perform_create(self, serializer):
    #     return serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        return serializer.save(updated_by=self.request.user)
