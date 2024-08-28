
from django.urls import path

from fs_utils.exporter.views import ExportDataView
from fs_utils.importer.views import ImportDataView
from fs_utils.notifications.emails import *
from fs_utils.utils import generate_secret_token

urlpatterns = [
    path('send-email/', send_test_email,
         name='send_email'),
    path('secret-token/', generate_secret_token,
         name='secret-token'),
    path('export-data/', ExportDataView.as_view(), name='export-data'),
    path('import-data/', ImportDataView.as_view(), name='import-data'),
]
