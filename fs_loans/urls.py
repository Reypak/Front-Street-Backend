from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()

# define the router path and viewset to be used
router.register(r'loans', LoanViewSet, basename="Loans")

# specify URL Path for rest_framework
urlpatterns = [
    path('', include(router.urls)),
    path('schedule/<int:loan_id>/',
         LoanScheduleView.as_view(), name='loan_schedule', ),
]
