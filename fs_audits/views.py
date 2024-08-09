from rest_framework import generics

from fs_audits.filters import AuditTrailFilterSet
from fs_utils.filters.filter_backends import DEFAULT_FILTER_BACKENDS
from .models import AuditTrail
from .serializers import AuditTrailSerializer
from rest_framework.permissions import IsAuthenticated


class AuditTrailListCreateView(generics.ListAPIView):
    """
    An API for listing audit trails for all activities
    """
    queryset = AuditTrail.objects.all().order_by('-created_at')
    serializer_class = AuditTrailSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = DEFAULT_FILTER_BACKENDS
    filterset_class = AuditTrailFilterSet
