from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


class MyTokenObtainPairView(TokenObtainPairView):
    # Optionally, you can customize the view
    pass


class MyTokenRefreshView(TokenRefreshView):
    # Optionally, you can customize the view
    pass
