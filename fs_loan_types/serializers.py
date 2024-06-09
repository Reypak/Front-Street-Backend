from fs_documents.serializers import DocumentSerializer
from .models import LoanType
from fs_utils.serializers import BaseSerializer


class LoanTypeSerializer(BaseSerializer):

    attachments = DocumentSerializer(many=True, required=False)

    class Meta:
        model = LoanType
        fields = '__all__'

        # read_only_fields = ['created_by']
        # fields = ['id', 'borrower_name', 'phone', 'amount', 'status']
