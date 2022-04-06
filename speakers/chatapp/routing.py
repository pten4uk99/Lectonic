
from django.urls import re_path, path

from .consumers import ChatConsumer, NotificationsConsumer

websocket_urlpatterns = [
    path('ws/connect/<int:pk>', NotificationsConsumer.as_asgi()),
    path('ws/chat/<int:pk>', ChatConsumer.as_asgi())
]