from django.apps import AppConfig

class MessagingAppConfig(AppConfig):
    name = 'messaging_app'

    def ready(self):
        import messaging.signals
