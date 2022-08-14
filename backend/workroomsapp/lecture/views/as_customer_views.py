from drf_yasg.utils import swagger_auto_schema

from authapp.models import User
from services.api import service_delete_lecture_by_id
from services.filters import CreatedCustomerLectureFilter
from services.filters.lecture import WithoutPermanentLectureFilter, FutureLectureFilter
from workroomsapp.generics import ListCreateAPIView, UpdateDeleteAPIView
from workroomsapp.lecture.lecture_serializers import LectureAsCustomerSerializer
from workroomsapp.models import Lecture
from workroomsapp.query_serializers import LectureGetParamsSerializer
from workroomsapp.utils import workroomsapp_permissions


class LectureAsCustomerListCreateAPIView(ListCreateAPIView):
    queryset = Lecture.objects.all()
    filter_classes = [CreatedCustomerLectureFilter,
                      FutureLectureFilter,
                      WithoutPermanentLectureFilter]
    serializer_class = LectureAsCustomerSerializer
    query_serializer_class = LectureGetParamsSerializer
    permission_classes = [workroomsapp_permissions.IsCustomer |
                          workroomsapp_permissions.IsLecturer]
    
    @swagger_auto_schema(operation_summary='Создание лекции от имени заказчика',
                         request_body=LectureAsCustomerSerializer)
    def post(self, request, *args, **kwargs):
        return super().post(request)
    
    def get_from_obj(self):
        query = self.get_query()
        user = User.objects.get(pk=query['user_id'])
        
        if not user.lecturer:
            raise self.get_error()
        return user
    
    @swagger_auto_schema(operation_summary='Получение списка лекций от имени заказчика',
                         query_serializer=LectureGetParamsSerializer())
    def get(self, request, *args, **kwargs):
        return super().get(request)


class LectureAsCustomerUpdateDeleteAPIView(UpdateDeleteAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureAsCustomerSerializer
    permission_classes = [workroomsapp_permissions.IsCustomer]
    
    @swagger_auto_schema(operation_summary='Редактирование лекции от имени заказчика',
                         request_body=LectureAsCustomerSerializer)
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_summary='Удаление лекции от имени заказчика')
    def delete(self, request, pk, *args, **kwargs):
        service_delete_lecture_by_id(from_obj=self.request.user, lecture_id=pk)
        return super().delete(request, *args, **kwargs)
