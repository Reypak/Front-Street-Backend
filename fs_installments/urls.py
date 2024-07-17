
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()

# define the router path and viewset to be used
router.register(r'installments', InstallmentViewSet, basename="Installments")

urlpatterns = [
    path('', include(router.urls)),

    path('schedule/', PaymentScheduleCreateView.as_view(), name='payment_schedule'),

    path('schedule/<int:loan_id>/',
         PaymentScheduleView.as_view(), name='payment_schedule'),

    path('installments/loan/<int:loan_id>/', LoanInstallmentList.as_view(),
         name='loan_installment_list'),
]
