
from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import CalculateInstallmentsView, LoanInstallmentCreateView

from .views import *

router = SimpleRouter()

# define the router path and viewset to be used
router.register(r'', InstallmentViewSet, basename="Installments")

urlpatterns = [
    path('installments/', include(router.urls)),
    path('calculate_installments/', CalculateInstallmentsView.as_view(),
         name='calculate_installments'),
    path('create_installments/', LoanInstallmentCreateView.as_view(),
         name='loan_installment_create'),

]
