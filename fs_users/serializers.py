from rest_framework import serializers
from fs_users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    role_name = serializers.CharField(source="role.name", read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id',
                  'email',
                  'first_name',
                  'last_name',
                  'phone_number',
                  'role',
                  'role_name',
                  'is_staff',
                  'display_name',
                  'is_active',
                  'date_joined',
                  'last_login',
                  'permissions'
                  ]

    def get_permissions(self, obj):
        # get permissions from role
        return list(obj.role.permissions.values_list('codename', flat=True))
