from django.core import exceptions
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from services.filters import CreatedCustomerLectureFilter
from workroomsapp.lecture import lecture_responses
from workroomsapp.lecture.lecture_serializers import LectureAsCustomerSerializer, LecturesGetSerializer
from workroomsapp.models import Customer, Lecture
from workroomsapp.utils import workroomsapp_permissions


class LectureAsCustomerAPIView(APIView):
    permission_classes = [workroomsapp_permissions.IsCustomer |
                          workroomsapp_permissions.IsLecturer]
    
    def get_customer(self, id_):
        customer = Customer.objects.filter(person__user_id=id_).first()
        if not customer:
            raise exceptions.ObjectDoesNotExist('Объекта не существует в базе данных')
        return customer
    
    @swagger_auto_schema(deprecated=True)
    def post(self, request):
        serializer = LectureAsCustomerSerializer(data=request.data, context={'request': request})
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
            user = self.get_customer(user_id).person.user
        
        filter_class = CreatedCustomerLectureFilter(from_obj=user, city=city, domain=domain)
        serializer = LecturesGetSerializer(filter_class.filter(), many=True, context={'user': user})
        return lecture_responses.success_get_lectures(serializer.data)
    
    @swagger_auto_schema(deprecated=True)
    def patch(self, request):
        lecture_id = request.data.get('id')
        
        lecture = Lecture.objects.filter(pk=lecture_id).first()
        
        if not lecture or not lecture.customer or lecture.customer.person.user != request.user:
            return lecture_responses.forbidden()
        
        serializer = LectureAsCustomerSerializer(
            lecture, data=request.data, context={'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return lecture_responses.success_get_lectures([])
