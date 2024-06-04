from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()

# define the router path and viewset to be used
router.register(r'', LoanTypeViewSet, basename="Loan Types")

# specify URL Path for rest_framework
urlpatterns = [
    path('loan_types/', include(router.urls)),
]
