from django.apps import AppConfig


class FsInstallmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fs_installments'

    def ready(self):
        import fs_installments.signals
