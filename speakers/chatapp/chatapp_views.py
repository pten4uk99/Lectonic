from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from chatapp import chatapp_responses
from chatapp.chatapp_serializers import *
from chatapp.models import Chat, Message, WsClient
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

    def get_chat(self, chat_id):
        chat = Chat.objects.filter(pk=chat_id).first()

        if not chat:
            return chatapp_responses.chat_does_not_exist()
        return chat

    def get_respondent(self, talker_person):
        if not talker_person:
            respondent = False
        else:
            respondent = talker_person.pk

        return respondent

    def get_is_creator(self, lecture):
        """ Проверяет является ли пользователь создателем лекции """

        is_creator = None

        if lecture.lecturer:
            is_creator = lecture.lecturer.person.user == self.request.user
        elif lecture.customer:
            is_creator = lecture.customer.person.user == self.request.user

        return is_creator

    def handle_messages(self, chat):
        """
        Обрабатывает сообщения в чате:
        делает их все прочитанными и проверяет
        есть ли подтвержденное/отклоненное сообщение (подтверждение/отклонение лекции).

        Возвращает кортеж: (полный список сообщений чата, есть ли подтвержденное или отклоненное сообщение)
         """

        messages = Message.objects.order_by('datetime').filter(chat=chat)
        other_messages = messages.exclude(author=self.request.user)

        lecture_confirmed = None

        for message in messages:  # Проверяем наличие подтвержденного или отклоненного сообщения
            if lecture_confirmed is not None:
                continue
            if message.confirm is None:
                lecture_confirmed = None
            else:
                lecture_confirmed = message.confirm

        for message in other_messages:
            message.need_read = False  # Читаем сообщения
            message.save()

        return messages, lecture_confirmed

    def send_ws_message(self, client, message):
        WsClient([client], message)

    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        chat_id = request.GET.get('chat_id')
        if not chat_id:
            chatapp_responses.chat_id_not_in_data()

        chat = self.get_chat(chat_id)
        lecture = chat.lecture
        talker_person = chat.users.exclude(pk=request.user.pk).first().person
        respondent = self.get_respondent(talker_person)
        is_creator = self.get_is_creator(lecture)
        messages, lecture_confirmed = self.handle_messages(chat)

        ws_client = getattr(talker_person.user, 'ws_client', None)
        if ws_client:
            self.send_ws_message(
                ws_client,
                {
                    'type': 'read_messages',
                    'chat_id': chat_id,
                })

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

