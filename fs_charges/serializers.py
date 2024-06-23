
from fs_charges.models import Charge
from fs_utils.serializers import BaseSerializer


class ChargeSerializer(BaseSerializer):
    class Meta:
        model = Charge
        fields = '__all__'
