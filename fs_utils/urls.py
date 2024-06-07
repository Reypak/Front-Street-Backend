
from django.urls import path

from fs_utils.notifications.emails import send_email

urlpatterns = [
    path('send-email/', send_email,
         name='send_email'),
]
