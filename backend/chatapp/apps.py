from django.apps import AppConfig
from django.db import ProgrammingError


class ChatappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chatapp'

    def ready(self):
        """ Отчищает подключенных онлайн пользователей при каждом перезапуске бэкенда """

        from chatapp.models import WsClient

        try:
            WsClient.objects.all().delete()
        except ProgrammingError:
            pass
