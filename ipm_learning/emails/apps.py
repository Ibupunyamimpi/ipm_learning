from django.apps import AppConfig


class EmailsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ipm_learning.emails'

    def ready(self):
        # Implicitly connect a signal handlers decorated with @receiver.
        from . import signals