
from django.urls import path

from chatapp.consumers.consumers import ChatConsumer, NotificationsConsumer

websocket_urlpatterns = [
    path('ws/connect/<int:pk>', NotificationsConsumer.as_asgi()),
    path('ws/chat/<int:pk>', ChatConsumer.as_asgi())
]