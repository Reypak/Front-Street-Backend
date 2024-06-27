from rest_framework import serializers
from fs_roles.serializers import RoleSerializer
from fs_users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name',
                  'last_name', 'phone_number', 'role']
