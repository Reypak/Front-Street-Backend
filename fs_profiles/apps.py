from django.apps import AppConfig


class FsProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fs_profiles'

    def ready(self):
        import fs_profiles.signals
