from django.urls import path

from .views import *

urlpatterns = [
    path('comments/', CommentListView.as_view(),
         name='comment-list'),
    path('comments/<int:pk>/', CommentListView.as_view(),
         name='comment-list'),
]
