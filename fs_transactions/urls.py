from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import *

from .views import *

router = SimpleRouter()

# define the router path and viewset to be used
router.register(r'', TransactionViewSet, basename="Transactions")

# specify URL Path for rest_framework
urlpatterns = [
    path('transactions/', include(router.urls)),
    path('transactions/loan/<int:loan_id>/', TransactionList.as_view(),
         name='transaction_list'),
]
