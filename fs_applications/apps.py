from django.apps import AppConfig


class FsApplicationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fs_applications'

    def ready(self):
        import fs_applications.signals
