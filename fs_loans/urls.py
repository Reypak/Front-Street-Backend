from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()

# define the router path and viewset to be used
router.register(r'loans', LoanViewSet, basename="Loans")

# specify URL Path for rest_framework
urlpatterns = [
    path('', include(router.urls)),
    path('loans/<int:loan_id>/statement/',
         download_loan_statement, name='loan_statement'),
]
