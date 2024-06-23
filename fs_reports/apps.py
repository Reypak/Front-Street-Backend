from django.apps import AppConfig


class FsReportsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fs_reports'

    # def ready(self):
    #     import fs_loan_reports.signals
