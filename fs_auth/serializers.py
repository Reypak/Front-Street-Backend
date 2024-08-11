# from django.utils import timezone
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)

#         # Update last_login field
#         self.user.last_login = timezone.now()
#         self.user.save(update_fields=['last_login'])

#         return data

from rest_framework import serializers
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode

from fs_users.models import CustomUser
from fs_utils.constants import FROM_EMAIL, SITE_URL
from fs_utils.notifications.emails import send_templated_email


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            self.user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                "There is no user registered with this email address.")
        return value

    def save(self):
        user = self.user
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"{SITE_URL}{'reset-password/'}{uid}/{token}/"

        # Send the email
        subject = "Password Reset Requested"

        context = {
            'name': user.first_name,
            'reset_link': reset_link
        }

        return send_templated_email(subject, 'password_reset.html', context, [user.email])


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            uid = urlsafe_base64_decode(attrs['uid']).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            raise serializers.ValidationError("Invalid user ID")

        if not default_token_generator.check_token(user, attrs['token']):
            raise serializers.ValidationError("Invalid or expired token")

        attrs['user'] = user
        return attrs

    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
