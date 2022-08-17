from django.apps import AppConfig


class BaseAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'baseapp'

    def ready(self):
        import baseapp.signals
