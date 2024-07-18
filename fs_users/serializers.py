from rest_framework import serializers
from fs_roles.serializers import RoleSerializer
from fs_users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    # role_details = RoleSerializer(source="role", read_only=True)

    role_name = serializers.CharField(source="role.name", read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id',
                  'role',
                  'email',
                  'first_name',
                  'last_name',
                  'phone_number',
                  'role_name',
                  'is_staff',
                  'display_name',
                  'is_active',
                  'date_joined',
                  'last_login',
                  #   'role_details'
                  ]
