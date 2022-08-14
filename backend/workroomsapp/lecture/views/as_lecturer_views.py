import logging

from channels.layers import get_channel_layer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from authapp.models import User
from services.api import service_delete_lecture_by_id, \
    service_response_to_lecture, service_cancel_response_to_lecture, service_confirm_respondent_to_lecture, \
    service_reject_respondent_to_lecture
from services.filters import CreatedLecturerLectureFilter, FutureLectureFilter
from services.filters.lecture import WithoutPermanentLectureFilter
from workroomsapp.generics import ListCreateAPIView, UpdateDeleteAPIView, DetailAPIView
from workroomsapp.lecture import lecture_responses
from workroomsapp.lecture.lecture_serializers import LectureAsLecturerSerializer, LecturesGetSerializer
from workroomsapp.models import Lecture
from workroomsapp.query_serializers import LectureGetParamsSerializer
from workroomsapp.utils import workroomsapp_permissions

channel_layer = get_channel_layer()
logger = logging.getLogger(__name__)


class LectureAsLecturerListCreateAPIView(ListCreateAPIView):
    queryset = Lecture.objects.all()
    filter_classes = [CreatedLecturerLectureFilter,
                      FutureLectureFilter,
                      WithoutPermanentLectureFilter]
    serializer_class = LectureAsLecturerSerializer
    query_serializer_class = LectureGetParamsSerializer
    permission_classes = [workroomsapp_permissions.IsCustomer |
                          workroomsapp_permissions.IsLecturer]
    
    @swagger_auto_schema(operation_summary='Создание лекции от имени лектора',
                         request_body=LectureAsLecturerSerializer,
                         responses={201: ''})
    def post(self, request, *args, **kwargs):
        return super().post(request)
    
    def get_from_obj(self):
        query = self.get_query()
        
        if query.get('user_id', None):
            user = User.objects.filter(pk=query['user_id']).first()
            if not user or not user.person.lecturer:
                raise self.get_error()
        else:
            user = self.request.user
        
        return user
    
    @swagger_auto_schema(operation_summary='Получение списка созданных лекций от имени лектора',
                         query_serializer=LectureGetParamsSerializer())
    def get(self, request, *args, **kwargs):
        return super().get(request)


class LectureAsLecturerUpdateDeleteAPIView(UpdateDeleteAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureAsLecturerSerializer
    permission_classes = [workroomsapp_permissions.IsLecturer]
    
    @swagger_auto_schema(operation_summary='Редактирование лекции от имени лектора',
                         request_body=LectureAsLecturerSerializer)
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_summary='Удаление лекции от имени лектора')
    def delete(self, request, pk, *args, **kwargs):
        service_delete_lecture_by_id(from_obj=self.request.user, lecture_id=pk)
        return super().delete(request, *args, **kwargs)


class LectureDetailAPIView(DetailAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LecturesGetSerializer
    
    @swagger_auto_schema(operation_summary='Детальное описание лекции')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


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
