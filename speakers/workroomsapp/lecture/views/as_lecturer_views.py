import logging

from channels.layers import get_channel_layer
from django.db import transaction
from django.db.models import Max, Min
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from chatapp.chatapp_serializers import ChatSerializer
from workroomsapp.lecture.docs import lecture_docs
from workroomsapp.lecture.serializers.as_lecturer_serializers import *
from workroomsapp.lecture.utils.response_on_lecture import *
from workroomsapp.models import Lecturer, Customer
from workroomsapp.utils import workroomsapp_permissions

channel_layer = get_channel_layer()
logger = logging.getLogger(__name__)


class LectureAsLecturerAPIView(APIView):
    permission_classes = [workroomsapp_permissions.IsLecturer |
                          workroomsapp_permissions.IsCustomer]

    @swagger_auto_schema(**lecture_docs.LectureAsLecturerCreateDoc)
    def post(self, request):
        serializer = LectureCreateAsLecturerSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return lecture_responses.lecture_created()

    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        lecturer_id = request.GET.get('id')
        created_lectures = []

        if not lecturer_id:
            if hasattr(request.user.person, 'lecturer'):
                created_lectures = request.user.person.lecturer.lectures.all()
        else:
            created_lectures = Lecturer.objects.get(pk=lecturer_id).lectures.all()

        lectures_list = []
        for lecture in created_lectures:
            lowest = lecture.lecture_requests.aggregate(maximum=Max('event__datetime_start'))
            lowest = lowest.get('maximum')
            if lowest > datetime.datetime.now(tz=datetime.timezone.utc):
                lectures_list.append(lecture)

        serializer = LecturesGetSerializer(
            lectures_list, many=True, context={'request': request})

        return lecture_responses.success_get_lectures(serializer.data)

    @swagger_auto_schema(deprecated=True)
    def delete(self, request):
        lecture_id = request.GET.get('lecture_id')

        if not lecture_id:
            lecture_responses.not_in_data()

        lecture = Lecture.objects.filter(pk=lecture_id).first()

        if not lecture:
            return lecture_responses.does_not_exist()

        if lecture.lecturer:
            if not lecture.lecturer.person.user == request.user:
                return lecture_responses.not_a_creator()
        elif lecture.customer:
            if not lecture.customer.person.user == request.user:
                return lecture_responses.not_a_creator()

        lecture.delete()
        return lecture_responses.lecture_deleted()


class LectureDetailAPIView(APIView):
    @swagger_auto_schema(deprecated=True)
    def get(self, request, pk):
        if not pk:
            return lecture_responses.not_in_data()

        lecture = Lecture.objects.filter(pk=pk)

        if not lecture.first():
            return lecture_responses.does_not_exist()

        serializer = LecturesGetSerializer(
            lecture, many=True, context={'request': request})

        return lecture_responses.success_get_lectures(serializer.data)


class LectureResponseAPIView(APIView, LectureResponseMixin):
    permission_classes = [workroomsapp_permissions.IsLecturer |
                          workroomsapp_permissions.IsCustomer]

    def add_respondent(self):
        for response_request in self.get_responses():
            response_request.respondents.add(self.request.user.person)
            response_request.save()
        logger.info(f'responses: {self.get_responses()}')

    def get_or_create_chat(self):
        responses = self.get_responses()
        chat = Chat.objects.filter(
            lecture_requests__in=responses, users=self.get_creator().user).filter(
            users=self.request.user).first()

        if not chat:
            chat = Chat.objects.create(lecture=self.get_lecture())
            chat.lecture_requests.add(*responses)
            chat.users.add(self.get_creator().user, self.request.user)
            chat.save()
        logger.info(f'chat: {chat}')
        return chat

    def create_response_message(self):
        dates = []
        for date in self.get_format_dates():
            dates.append(date.strftime('%d.%m'))

        message = Message.objects.create(
            author=self.request.user,
            chat=self.get_or_create_chat(),
            text=f'Собеседник заинтересован в Вашем предложении. '
                 f'Возможные даты проведения: {", ".join(dates)}.'
        )
        logger.info(f'text:{message.text}, author: {message.author}')

    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        with transaction.atomic():
            self.check_can_response()  # может ли пользователь откликаться на эту лекцию
            self.add_respondent()  # добавляем откликнувшегося к лекции
            chat = self.get_or_create_chat()
            self.create_response_message()  # создаем сообщение по умолчанию при отклике

            chat_serializer = ChatSerializer(chat, context={'request': request})

            self.send_ws_message(clients=[request.user, self.get_creator().user], message={
                'type': 'new_respondent',
                'chat': chat,
                'respondent_id': self.request.user.pk,
                **chat_serializer.data
            })  # отправляем сообщение обоим собеседникам чата

        return lecture_responses.success_response()


class LectureCancelResponseAPIView(APIView, LectureCancelResponseMixin):
    permission_classes = [workroomsapp_permissions.IsLecturer |
                          workroomsapp_permissions.IsCustomer]

    def remove_chat(self, lecture_request):
        chat_list = getattr(lecture_request, 'chat_list', None)

        if not chat_list:
            chats = Chat.objects.filter(lecture=self.get_lecture())

            for elem in chats:
                if elem.users.all().count() < 2:
                    elem.delete()

            return lecture_responses.success_cancel([{'type': 'chat_does_not_exist'}])

        chat = chat_list.filter(users=self.request.user).first()
        logger.info(f'chat: {chat}')
        chat_id = chat.pk
        users = []

        for user in chat.users.all():
            users.append(user)

        chat.delete()
        return chat_id, users

    def remove_respondent(self):
        user_list = []
        chat = None

        for lecture_request in self.get_lecture().lecture_requests.all():
            respondent_obj = lecture_request.respondent_obj.filter(person=self.request.user.person).first()

            if respondent_obj and not respondent_obj.rejected:
                lecture_request.respondents.remove(self.request.user.person)

                if not chat:
                    chat_id, users = self.remove_chat(lecture_request)

                user_list = users
                chat = chat_id
                lecture_request.save()
                logger.info(f'respondent_obj: {respondent_obj}, rejected: {respondent_obj.rejected}')

        return chat, user_list

    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        with transaction.atomic():
            self.check_can_response()
            chat_id, users = self.remove_respondent()  # удаляет откликнувшегося и
            # возвращает id и собеседников удаленного чата

            self.send_ws_message(clients=users, message={
                    'type': 'remove_respondent',
                    'chat_id': chat_id,
                })  # отправляем сообщение обоим собеседникам чата

        return lecture_responses.success_cancel()


class LectureConfirmRespondentAPIView(APIView, LectureConfirmRespondentMixin):
    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        self.check_is_creator()
        self.handle_respondent()  # обрабатываем откликнувшегося пользователя (подтверждаем, отклоняем)
        self.handle_message()
        return lecture_responses.success_confirm()


class LectureRejectRespondentAPIView(APIView, LectureRejectRespondentMixin):
    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        self.check_is_creator()
        self.handle_respondent()  # обрабатываем откликнувшегося пользователя (подтверждаем/отклоняем)
        self.handle_message()  # обрабатываем сообщение (объект Message): создаем, и отправляем по веб сокету
        return lecture_responses.success_denied()
