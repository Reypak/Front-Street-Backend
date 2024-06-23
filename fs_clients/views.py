from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from fs_clients.serializers import ClientSerializer
from .models import *


# Create your views here.
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ClientSerializer
