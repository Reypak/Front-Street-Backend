from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from fs_auth.serializers import MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    # Optionally, you can customize the view
    # pass


class MyTokenRefreshView(TokenRefreshView):
    # Optionally, you can customize the view
    pass
