
from django.urls import path

from fs_utils.notifications.emails import *

urlpatterns = [
    path('send-email/', send_test_email,
         name='send_email'),
]
