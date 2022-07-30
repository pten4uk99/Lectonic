import logging

from channels.layers import get_channel_layer
from django.core import exceptions
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from services.api import service_delete_lecture_by_id, \
    service_response_to_lecture, service_cancel_response_to_lecture, service_confirm_respondent_to_lecture, \
    service_reject_respondent_to_lecture
from services.filters import CreatedLecturerLectureFilter
from workroomsapp.lecture import lecture_responses
from workroomsapp.lecture.docs import lecture_docs
from workroomsapp.lecture.lecture_serializers import LectureAsLecturerSerializer, LecturesGetSerializer
from workroomsapp.models import Lecturer, Lecture
from workroomsapp.utils import workroomsapp_permissions

channel_layer = get_channel_layer()
logger = logging.getLogger(__name__)


class LectureAsLecturerAPIView(APIView):
    permission_classes = [workroomsapp_permissions.IsLecturer |
                          workroomsapp_permissions.IsCustomer]

    def get_lecturer(self, id_):
        lecturer = Lecturer.objects.filter(person__user_id=id_).first()
        if not lecturer:
            raise exceptions.ObjectDoesNotExist('Объекта не существует в базе данных')
        return lecturer

    @swagger_auto_schema(**lecture_docs.LectureAsLecturerCreateDoc)
    def post(self, request):
        serializer = LectureAsLecturerSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return lecture_responses.lecture_created()

    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        user_id = request.GET.get('user_id')
        city = request.GET.get('city', '')
        domain = request.GET.get('domain', '')

        user = request.user
        if user_id:
            user = self.get_lecturer(user_id).person.user

        filter_class = CreatedLecturerLectureFilter(from_obj=user, city=city, domain=domain)
        serializer = LecturesGetSerializer(filter_class.filter(), many=True, context={'user': user})
        return lecture_responses.success_get_lectures(serializer.data)

    @swagger_auto_schema(deprecated=True)
    def patch(self, request):
        lecture_id = request.data.get('id')

        lecture = Lecture.objects.filter(pk=lecture_id).first()
        if not lecture or lecture.lecturer.person.user != request.user:
            return lecture_responses.forbidden()

        serializer = LectureAsLecturerSerializer(
            lecture, data=request.data, context={'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return lecture_responses.success_get_lectures([])

    @swagger_auto_schema(deprecated=True)
    def delete(self, request):
        lecture_id = request.GET.get('lecture_id')

        if not lecture_id:
            lecture_responses.not_in_data()

        service_delete_lecture_by_id(from_obj=request.user, lecture_id=lecture_id)
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
            lecture, many=True, context={'user': request.user})

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

        service_response_to_lecture(request.user, lecture_id, dates)

        return lecture_responses.success_response()


class LectureCancelResponseAPIView(APIView):
    permission_classes = [workroomsapp_permissions.IsLecturer |
                          workroomsapp_permissions.IsCustomer]

    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        lecture_id: int = self.request.GET.get('lecture')

        if not lecture_id:
            return lecture_responses.not_in_data()

        service_cancel_response_to_lecture(request.user, lecture_id=lecture_id)

        return lecture_responses.success_cancel()


class LectureConfirmRespondentAPIView(APIView):
    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        respondent_id = self.request.GET.get('respondent')
        chat_id = self.request.GET.get('chat_id')

        if not (respondent_id and chat_id):
            return lecture_responses.not_in_data()

        service_confirm_respondent_to_lecture(request.user, chat_id, respondent_id)
        return lecture_responses.success_confirm()


class LectureRejectRespondentAPIView(APIView):
    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        respondent_id = self.request.GET.get('respondent')
        chat_id = self.request.GET.get('chat_id')

        if not (respondent_id and chat_id):
            return lecture_responses.not_in_data()

        service_reject_respondent_to_lecture(request.user, chat_id, respondent_id)
        return lecture_responses.success_denied()
