from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()

# define the router path and viewset to be used
router.register(r'loan_types', LoanTypeViewSet, basename="Loan Types")

# specify URL Path for rest_framework
urlpatterns = [
    path('', include(router.urls)),
]
