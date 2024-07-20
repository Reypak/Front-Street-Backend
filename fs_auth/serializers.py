# from django.utils import timezone
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)

#         # Update last_login field
#         self.user.last_login = timezone.now()
#         self.user.save(update_fields=['last_login'])

#         return data
