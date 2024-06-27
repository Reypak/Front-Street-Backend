
from django.urls import include, path
# from rest_framework.routers import SimpleRouter
from .views import *

# router = SimpleRouter()
# router.register(r'users', UserViewSet, basename="Users")

urlpatterns = [
    # path('', include(router.urls)),
    path('create_user/', CreateUserAPIView.as_view(), name='create_user'),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
