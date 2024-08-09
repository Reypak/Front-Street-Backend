from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()

urlpatterns = [
    path('audit-trail/', AuditTrailListCreateView.as_view(),
         name='audit-trail-list'),
]
