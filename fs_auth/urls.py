from django.urls import path
from .views import MyTokenObtainPairView, MyTokenRefreshView, PasswordResetConfirmView, PasswordResetView

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset/', PasswordResetView.as_view(),
         name='password_reset'),
    path('reset-password/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

]
