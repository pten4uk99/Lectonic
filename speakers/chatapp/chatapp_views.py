from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from chatapp import chatapp_responses
from chatapp.chatapp_serializers import *
from chatapp.models import Chat, Message
from workroomsapp.utils import workroomsapp_permissions


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

        chat = Chat.objects.filter(pk=chat_id).first()
        if not chat:
            chatapp_responses.chat_does_not_exist()

        messages = Message.objects.order_by('datetime').filter(chat=chat)
        for message in messages:
            message.need_read = False
            message.save()

        lecture = chat.lecture_request.lecture
        talker_person = chat.users.exclude(pk=request.user.pk).first().person
        respondent = talker_person.respondents.filter(lecture_requests=chat.lecture_request).first()
        if not respondent:
            respondent = False
        else:
            respondent = respondent.pk

        is_creator = False

        if chat.lecture.lecturer:
            is_creator = chat.lecture.lecturer.person.user == request.user
        elif chat.lecture.customer:
            is_creator = chat.lecture.customer.person.user == request.user

        serializer = MessageSerializer(messages, many=True)
        return chatapp_responses.success([{
            'lecture_id': lecture.pk,
            'lecture_name': lecture.name,
            'is_creator': is_creator,
            'talker_respondent': respondent,
            'talker_first_name': talker_person.first_name,
            'talker_last_name': talker_person.last_name,
            'messages': serializer.data,
        }])
