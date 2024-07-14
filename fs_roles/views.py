from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Role
from .serializers import PermissionSerializer, RoleSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class RoleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Role.objects.all().order_by('-id')
    serializer_class = RoleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_create(self, serializer):
        permissions = serializer.validated_data.pop('permissions', [])
        role = serializer.save()
        role.permissions.set(permissions)

    def perform_update(self, serializer):
        permissions = serializer.validated_data.pop('permissions', [])
        role = serializer.save()
        role.permissions.set(permissions)


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None  # Disable pagination for this viewset

    def get_queryset(self):
        # Get content types for admin, sessions, contenttypes, and auth
        excluded_apps = ['admin', 'sessions', 'contenttypes', 'auth']
        excluded_content_types = ContentType.objects.filter(
            app_label__in=excluded_apps)
        return Permission.objects.exclude(content_type__in=excluded_content_types)
