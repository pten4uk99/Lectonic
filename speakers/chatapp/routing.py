
from django.urls import path

from chatapp.consumers.chat_consumer import ChatConsumer
from chatapp.consumers.notificatioins_consumer import NotificationsConsumer

websocket_urlpatterns = [
    path('ws/connect/<int:pk>', NotificationsConsumer.as_asgi()),
    path('ws/chat/<int:pk>', ChatConsumer.as_asgi())
]