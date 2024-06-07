from django.urls import include, path
from rest_framework.routers import SimpleRouter

from fs_payments.views import LoanPaymentViewSet

from .views import *

router = SimpleRouter()

# define the router path and viewset to be used
router.register(r'loans', LoanPaymentViewSet, basename="Loan Payments")

# specify URL Path for rest_framework
urlpatterns = [
    path('payments/', include(router.urls)),
]
