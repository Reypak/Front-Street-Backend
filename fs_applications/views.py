from rest_framework import viewsets

from fs_applications.filters import ApplicationFilterSet
from fs_applications.models import Application
from fs_applications.serializers import *
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    permission_classes = [IsAuthenticated]
    # serializer_class = ApplicationSerializer
    filterset_class = ApplicationFilterSet

    def get_queryset(self):
        user = self.request.user
        if user.is_staff is True:
            # show all for staff
            queryset = Application.objects.all()
        else:
            # show only for client
            queryset = Application.objects.filter(client=user)
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return ApplicationListSerializer
        return ApplicationSerializer

    def perform_update(self, serializer):
        # pass request user
        return serializer.save(updated_by=self.request.user)
