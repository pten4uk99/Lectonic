from channels.layers import get_channel_layer
from django.core import exceptions
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from chatapp.chatapp_serializers import ChatSerializer
from workroomsapp.lecture.docs import lecture_docs
from workroomsapp.lecture.serializers.as_lecturer_serializers import *
from workroomsapp.lecture.services.api import serialize_created_lectures, service_delete_lecture_by_id, \
    service_response_to_lecture
from workroomsapp.lecture.services.filters import AttrNames
from workroomsapp.lecture.services.response_on_lecture import *
from workroomsapp.utils import workroomsapp_permissions

channel_layer = get_channel_layer()
logger = logging.getLogger(__name__)


class LectureAsLecturerAPIView(APIView):
    permission_classes = [workroomsapp_permissions.IsLecturer |
                          workroomsapp_permissions.IsCustomer]

    def get_lecturer(self, id_):
        lecturer = Lecturer.objects.filter(pk=id_).first()
        if not lecturer:
            raise exceptions.ObjectDoesNotExist('Объекта не существует в базе данных')
        return lecturer

    @swagger_auto_schema(**lecture_docs.LectureAsLecturerCreateDoc)
    def post(self, request):
        serializer = LectureCreateAsLecturerSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return lecture_responses.lecture_created()

    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        lecturer_id = request.GET.get('id')

        person = request.user.person
        if lecturer_id:
            person = self.get_lecturer(lecturer_id).person

        serializer = serialize_created_lectures(request, person, from_attr=AttrNames.LECTURER)
        return lecture_responses.success_get_lectures(serializer.data)

    @swagger_auto_schema(deprecated=True)
    def delete(self, request):
        lecture_id = request.GET.get('lecture_id')

        if not lecture_id:
            lecture_responses.not_in_data()

        service_delete_lecture_by_id(user=request.user, lecture_id=lecture_id)
        return lecture_responses.lecture_deleted()


class LectureDetailAPIView(APIView):
    @swagger_auto_schema(deprecated=True)
    def get(self, request, pk):
        if not pk:
            return lecture_responses.not_in_data()

        lecture = Lecture.objects.filter(pk=pk)
        # .first() сразу не берется, чтобы в сериализатор передавался Queryset,
        # а не один объект Lecture

        if not lecture.first():
            return lecture_responses.does_not_exist()

        serializer = LecturesGetSerializer(
            lecture, many=True, context={'request': request})

        return lecture_responses.success_get_lectures(serializer.data)


class LectureResponseAPIView(APIView):
    permission_classes = [workroomsapp_permissions.IsLecturer |
                          workroomsapp_permissions.IsCustomer]

    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        lecture_id: int = self.request.GET.get('lecture')
        dates: list[str] = self.request.GET.getlist('date')

        if not lecture_id or not dates:
            return lecture_responses.not_in_data()

        service_response_to_lecture(request, lecture_id, dates)

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
        self.check_is_possible()  # проверяем возможно ли подтвердить пользователя на выбранные даты
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
