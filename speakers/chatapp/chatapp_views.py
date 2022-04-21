from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from chatapp import chatapp_responses
from chatapp.chatapp_serializers import *
from chatapp.models import Chat, Message
from workroomsapp.utils import workroomsapp_permissions

channel_layer = get_channel_layer()


class ChatListGetAPIView(APIView):
    permission_classes = [workroomsapp_permissions.IsLecturer |
                          workroomsapp_permissions.IsCustomer]

# ---------------------- Пока не работает вебсокет --------------------------------
    @swagger_auto_schema(deprecated=True)
    def delete(self, request):
        chat_id = request.GET.get('chat_id')
        chat = Chat.objects.get(pk=chat_id)
        chat.delete()
        return chatapp_responses.success([{'chat': chat_id}])
# ---------------------- Пока не работает вебсокет --------------------------------

    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        chat = Chat.objects.filter(users__pk=request.user.pk)

        serializer = ChatSerializer(
            chat, many=True, context={'request': request})

        return chatapp_responses.success(serializer.data)


class MessageListGetAPIView(APIView):
    permission_classes = [workroomsapp_permissions.IsLecturer |
                          workroomsapp_permissions.IsCustomer]

# -------------- Пока не настроен вебсокет --------------------------------
    @swagger_auto_schema(deprecated=True)
    def post(self, request):
        chat_id = request.data['chat_id']

        messages = Message.objects.filter(chat_id=chat_id)
        other_messages = messages.exclude(author=request.user)
        for message in other_messages:
            message.need_read = False
            message.save()
        if messages.count() > 500:
            messages.first().delete()

        message = Message.objects.create(
            author=request.user,
            chat=Chat.objects.get(pk=chat_id),
            text=request.data['text'],
            confirm=request.data.get('confirm')
        )

        return chatapp_responses.success([{'text': message.text}])
# -------------- Пока не настроен вебсокет --------------------------------

    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        chat_id = request.GET.get('chat_id')
        if not chat_id:
            chatapp_responses.chat_id_not_in_data()

        chat = Chat.objects.filter(pk=chat_id).first()
        if not chat:
            return chatapp_responses.chat_does_not_exist()

        lecture = chat.lecture
        talker_person = chat.users.exclude(pk=request.user.pk).first().person
        if not talker_person:
            respondent = False
        else:
            respondent = talker_person.pk

        is_creator = False

        if chat.lecture.lecturer:
            is_creator = chat.lecture.lecturer.person.user == request.user
        elif chat.lecture.customer:
            is_creator = chat.lecture.customer.person.user == request.user

        lecture_confirmed = None

        messages = Message.objects.order_by('datetime').filter(chat=chat)
        other_messages = messages.exclude(author=request.user)
        for message in messages:
            if lecture_confirmed is not None:
                continue
            if message.confirm is None:
                lecture_confirmed = None
            else:
                lecture_confirmed = message.confirm

        for message in other_messages:
            message.need_read = False
            message.save()

        serializer = MessageSerializer(messages, many=True)
        return chatapp_responses.success([{
            'lecture_id': lecture.pk,
            'lecture_name': lecture.name,
            'is_creator': is_creator,
            'confirmed': lecture_confirmed,
            'response_dates': chat.lecture_requests.all().values_list(
                'event__datetime_start', 'event__datetime_end'),
            'talker_respondent': respondent,
            'talker_first_name': talker_person.first_name,
            'talker_last_name': talker_person.last_name,
            'messages': serializer.data,
        }])

