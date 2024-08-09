
from django.urls import path
from .views import *

urlpatterns = [
    path('create-user/', CreateUserAPIView.as_view(), name='create-user'),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
