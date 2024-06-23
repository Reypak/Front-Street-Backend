from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()

# define the router path and viewset to be used
router.register(r'clients', ClientViewSet, basename="Clients")

# specify URL Path for rest_framework
urlpatterns = [
    path('', include(router.urls)),
]
