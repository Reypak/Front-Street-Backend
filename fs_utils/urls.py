
from django.urls import path

from fs_utils.notifications.emails import *
from fs_utils.utils import generate_secret_token

urlpatterns = [
    path('send-email/', send_test_email,
         name='send_email'),
    path('secret-token/', generate_secret_token,
         name='secret-token'),
]
