from rest_framework import viewsets

from fs_charges.filters import *
from fs_charges.models import *
from rest_framework.permissions import IsAuthenticated
from fs_charges.serializers import *

# Create your views here.


class ChargeViewSet(viewsets.ModelViewSet):
    queryset = Charge.objects.all().order_by('-created_at')
    permission_classes = [IsAuthenticated]
    serializer_class = ChargeSerializer
    filterset_class = ChargeFilterSet


class ChargePenaltyViewSet(viewsets.ModelViewSet):
    queryset = ChargePenalty.objects.all().order_by('id')
    permission_classes = [IsAuthenticated]
    serializer_class = ChargePenaltySerializer
    filterset_class = ChargePenaltyFilterSet
