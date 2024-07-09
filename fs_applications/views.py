from rest_framework import viewsets

from fs_applications.filters import ApplicationFilterSet
from fs_applications.models import Application
from fs_applications.serializers import ApplicationSerializer
from fs_utils.filters.filter_backends import DEFAULT_FILTER_BACKENDS
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all().order_by('-created_at')
    permission_classes = [IsAuthenticated]
    serializer_class = ApplicationSerializer
    filter_backends = DEFAULT_FILTER_BACKENDS
    filterset_class = ApplicationFilterSet

    def perform_update(self, serializer):
        # pass request user
        return serializer.save(updated_by=self.request.user)
