from django.urls import path

from fs_reports.views import ReportSummary


urlpatterns = [
    path('reports/summary/', ReportSummary.as_view(), name='report-summary'),
]
