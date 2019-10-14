from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'

    # we need to make sure this file in signals.py is
    # initialized when the Django application is launched
    def ready(self):
        from main import signals
