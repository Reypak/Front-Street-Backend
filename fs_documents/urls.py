from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()

# define the router path and viewset to be used
router.register(r'', DocumentViewSet, basename="Documents")

# specify URL Path for rest_framework
urlpatterns = [
    path('documents/', include(router.urls)),
]
