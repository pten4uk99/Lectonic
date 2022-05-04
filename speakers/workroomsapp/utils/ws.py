from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from chatapp.models import WsClient


class WsMessageSender:
    channel_layer = get_channel_layer()

    def __init__(self, clients: list, message: dict):
        self.message = message
        self.clients = WsClient.objects.filter(user__in=clients)

    def send(self):
        for client in self.clients:
            async_to_sync(self.channel_layer.send)(getattr(client, 'channel_name', ''), self.message)
