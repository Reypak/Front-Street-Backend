
from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import *

router = SimpleRouter()

# define the router path and viewset to be used
router.register(r'users', UserViewSet, basename="Users")

urlpatterns = [
    path('', include(router.urls)),
]


# from django.urls import path

# from fs_users.views import *


# urlpatterns = [
#     path('users/', UserListCreateView.as_view(), name='user-list-create'),
#     path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
# ]
