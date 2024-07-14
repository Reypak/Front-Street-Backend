from rest_framework import serializers
from django.contrib.auth.models import Permission
from .models import Role


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']


class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    permission_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Permission.objects.all(), source='permissions'
    )

    class Meta:
        model = Role
        fields = ['id', 'name', 'permissions',
                  'permission_ids', 'created_at', 'updated_at']
