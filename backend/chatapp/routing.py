
from django.urls import path

from chatapp.consumers.consumers import WsConsumer

websocket_urlpatterns = [
    path('ws/connect/<int:pk>', WsConsumer.as_asgi()),
]
