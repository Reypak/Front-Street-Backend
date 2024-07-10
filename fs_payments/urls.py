from django.urls import include, path
from rest_framework.routers import SimpleRouter

from fs_payments.views import LoanPaymentViewSet

from .views import *

router = SimpleRouter()

# define the router path and viewset to be used
router.register(r'', LoanPaymentViewSet, basename="Payments")

# specify URL Path for rest_framework
urlpatterns = [
    path('payments/', include(router.urls)),
    path('payments/loan/<int:loan_id>/', LoanPaymentsList.as_view(),
         name='loan_payments_list'),
]
