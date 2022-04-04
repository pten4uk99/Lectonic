from django.urls import path

from chatapp.chatapp_views import *


urlpatterns = [
    path('chat_list/', ChatListGetAPIView.as_view()),
    path('message_list/', MessageListGetAPIView.as_view())
]
