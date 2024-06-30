
from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import LoanInstallmentCreateView

from .views import *

router = SimpleRouter()

# define the router path and viewset to be used
router.register(r'installments', InstallmentViewSet, basename="Installments")

urlpatterns = [
    path('', include(router.urls)),
    #     path('installments/loan/schedule/', LoanScheduleView.as_view(),
    #          name='loan_schedule'),
    path('installments/loan/create/', LoanInstallmentCreateView.as_view(),
         name='loan_installment_create'),
    path('installments/loan/<int:loan_id>/', LoanInstallmentList.as_view(),
         name='loan_installment_list'),
]
