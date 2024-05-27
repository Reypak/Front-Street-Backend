from rest_framework import viewsets
from utils.constants import CustomPagination

# Create your views here.
# import local data
from .serializers import LoanSerializer
from .models import Loan


# create a viewset
class LoanViewSet(viewsets.ModelViewSet):
    # define queryset
    queryset = Loan.objects.all()

    # specify serializer to be used
    serializer_class = LoanSerializer

    # for custom pagination
    # pagination_class = CustomPagination

    # def perform_create(self, serializer):
    #     return serializer.save(created_by=self.request.user)
