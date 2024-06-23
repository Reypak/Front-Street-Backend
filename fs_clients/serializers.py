
from fs_charges.models import Charge
from fs_clients.models import Client
from fs_utils.serializers import BaseSerializer


class ClientSerializer(BaseSerializer):
    class Meta:
        model = Client
        fields = '__all__'
