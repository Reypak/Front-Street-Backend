from django.apps import AppConfig


class FsLoansConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fs_loans'

    def ready(self):
        import fs_loans.signals
