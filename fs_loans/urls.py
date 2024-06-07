from django.urls import include, path
from rest_framework.routers import SimpleRouter

from fs_installments.views import CalculateInstallmentsView

from .views import *

router = SimpleRouter()

# define the router path and viewset to be used
router.register(r'', LoanViewSet, basename="Loans")

# specify URL Path for rest_framework
urlpatterns = [
    path('loans/', include(router.urls)),
    path('loan/calculate-installments/',
         CalculateInstallmentsView.as_view(), name='calculate-installments'),
]
