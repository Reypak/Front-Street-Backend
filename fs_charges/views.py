from rest_framework import viewsets

from fs_charges.models import Charge
from rest_framework.permissions import IsAuthenticated
from fs_charges.serializers import ChargeSerializer

# Create your views here.


class ChargeViewSet(viewsets.ModelViewSet):
    queryset = Charge.objects.all().order_by('-created_at')
    permission_classes = [IsAuthenticated]
    serializer_class = ChargeSerializer
