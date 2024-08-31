from rest_framework import serializers
from fs_profiles.serializer import ProfileSerializer
from fs_users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    role_name = serializers.CharField(source="role.name", read_only=True)
    profile = ProfileSerializer()

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
                  'permissions',
                  'profile'
                  ]

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        profile_serializer = self.fields['profile']

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        profile_instance = instance.profile
        profile_serializer.update(profile_instance, profile_data)

        return instance

    def get_permissions(self, obj):
        # get permissions from role
        return list(obj.role.permissions.values_list('codename', flat=True))


class UserListSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source="role.name", read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'display_name',
                  'phone_number', 'role_name', 'is_active',]
