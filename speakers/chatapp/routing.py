
from django.urls import re_path, path

from .consumers import ChatConsumer, NotificationsConsumer

websocket_urlpatterns = [
    path('connect/<int:pk>', NotificationsConsumer.as_asgi()),
    path('chat/<int:pk>', ChatConsumer.as_asgi())
]