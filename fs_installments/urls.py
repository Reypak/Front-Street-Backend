
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()

# define the router path and viewset to be used
router.register(r'installments', InstallmentViewSet, basename="Installments")

urlpatterns = [
    path('', include(router.urls)),

    path('schedule/', PaymentScheduleCreateView.as_view(),
         name='payment_schedule_create'),

    path('schedule/<int:loan_id>/',
         PaymentScheduleView.as_view(), name='payment_schedule_preview'),

    path('check_installments/', check_installments, name='check_installments'),

    path('send-reminders/', send_reminders, name='send-reminders'),

    path('reschedule/', RescheduleInstallmentView.as_view(),
         name='reschedule-installment'),
]
