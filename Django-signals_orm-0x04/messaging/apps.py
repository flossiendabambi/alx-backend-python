from django.apps import AppConfig

class MessagingAppConfig(AppConfig):
    name = 'messaging'

    def ready(self):
        import messaging.signals
