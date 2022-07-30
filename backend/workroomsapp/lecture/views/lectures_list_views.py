from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from services import AttrNames
from services.filters import ConfirmedLecturerLectureFilter, ConfirmedCustomerLectureFilter, \
    PotentialLecturerLectureFilter, PotentialCustomerLectureFilter
from workroomsapp.lecture import lecture_responses
from workroomsapp.lecture.lecture_serializers import LecturesGetSerializer


class LecturesGetAPIView(APIView):
    filter_class = None
    serializer_class = LecturesGetSerializer
    
    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        city = request.GET.get('city', '')
        domain = request.GET.get('domain', '')
        
        self.filter_class = self.filter_class(from_obj=request.user, city=city, domain=domain)
        serializer = self.serializer_class(self.filter_class.filter(), many=True, context={'user': request.user})
        return lecture_responses.success_get_lectures(serializer.data)


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
        
        filter_class = filter_class(from_obj=request.user, city=city, domain=domain)
        serializer = LecturesGetSerializer(filter_class.filter(), many=True, context={'user': request.user})
        return lecture_responses.success_get_lectures(serializer.data)


class PotentialLecturerLecturesGetAPIView(LecturesGetAPIView):
    filter_class = PotentialLecturerLectureFilter


class PotentialCustomerLecturesGetAPIView(LecturesGetAPIView):
    filter_class = PotentialCustomerLectureFilter
