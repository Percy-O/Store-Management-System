from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'


# Overriding the ready method
    def ready(self):
        import api.signals.handlers