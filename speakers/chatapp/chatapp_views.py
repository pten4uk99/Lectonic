from channels.layers import get_channel_layer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from chatapp import chatapp_responses
from chatapp.chatapp_serializers import *
from chatapp.models import Chat
from chatapp.services.api import serialize_chat_message_list
from workroomsapp.utils import workroomsapp_permissions

channel_layer = get_channel_layer()


class ChatListGetAPIView(APIView):
    permission_classes = [workroomsapp_permissions.IsLecturer |
                          workroomsapp_permissions.IsCustomer]

    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        chat = Chat.objects.filter(users__pk=request.user.pk)

        serializer = ChatSerializer(
            chat, many=True, context={'request': request})

        return chatapp_responses.success(serializer.data)


class MessageListGetAPIView(APIView):
    permission_classes = [workroomsapp_permissions.IsLecturer |
                          workroomsapp_permissions.IsCustomer]

    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        chat_id = request.GET.get('chat_id')
        if not chat_id:
            chatapp_responses.chat_id_not_in_data()

        serializer = serialize_chat_message_list(request, chat_id)
        return chatapp_responses.success(serializer.data)

