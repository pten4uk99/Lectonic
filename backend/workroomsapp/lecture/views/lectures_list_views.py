from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from services import AttrNames
from services.filters.lecture import *
from workroomsapp.generics import ListAPIView
from workroomsapp.lecture import lecture_responses
from workroomsapp.lecture.lecture_serializers import LecturesGetSerializer
from workroomsapp.models import Lecture
from workroomsapp.query_serializers import LecturesListGetParamsSerializer


class PermanentLecturesGetAPIView(ListAPIView):
    serializer_class = LecturesGetSerializer
    filter_classes = [PermanentLectureFilter]
    
    def get_from_obj(self):
        return self.request.user
    
    @swagger_auto_schema(operation_summary='Список созданных постоянных лекций')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ConfirmedLecturesGetAPIView(APIView):
    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        # чьи лекции берем
        obj_name = self.request.GET.get('obj_name')
        # от кого идет запрос
        query_from = AttrNames.LECTURER if obj_name == AttrNames.CUSTOMER.value else AttrNames.CUSTOMER
        
        city = request.GET.get('city', '')
        domain = request.GET.get('domain', '')
        
        if query_from == AttrNames.LECTURER:
            filter_class = ConfirmedLecturerLectureFilter
        else:
            filter_class = ConfirmedCustomerLectureFilter
        
        filter_class = filter_class(qs=Lecture.objects.all(), from_obj=request.user, city=city, domain=domain)
        serializer = LecturesGetSerializer(filter_class.filter(), many=True, context={'user': request.user})
        return lecture_responses.success_get_lectures(serializer.data)


class PotentialLecturesGetAPIView(ListAPIView):
    queryset = Lecture.objects.all()
    query_serializer_class = LecturesListGetParamsSerializer
    serializer_class = LecturesGetSerializer

    def get_from_obj(self):
        return self.request.user
    
    @swagger_auto_schema(operation_summary='Список потенциальных лекций',
                         query_serializer=LecturesListGetParamsSerializer())
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PotentialLecturerLecturesGetAPIView(PotentialLecturesGetAPIView):
    filter_classes = [WithoutLecturersLectureFilter,
                      FutureLectureFilter,
                      PotentialLecturerLectureFilter]


class PotentialCustomerLecturesGetAPIView(PotentialLecturesGetAPIView):
    filter_class = [WithoutCustomersLectureFilter,
                    FutureLectureFilter,
                    PotentialCustomerLectureFilter]
