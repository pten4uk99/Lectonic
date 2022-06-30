from django.core import exceptions
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from workroomsapp.lecture import lecture_responses
from workroomsapp.lecture.serializers.as_lecturer_serializers import *
from workroomsapp.lecture.api import serialize_created_lectures
from workroomsapp.lecture.filters import AttrNames
from workroomsapp.utils import workroomsapp_permissions


class LectureAsCustomerAPIView(APIView):
    permission_classes = [workroomsapp_permissions.IsCustomer]

    def get_customer(self, id_):
        customer = Customer.objects.filter(pk=id_).first()
        if not customer:
            raise exceptions.ObjectDoesNotExist('Объекта не существует в базе данных')
        return customer

    @swagger_auto_schema(deprecated=True)
    def post(self, request):
        serializer = LectureCreateAsCustomerSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return lecture_responses.lecture_created()

    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        customer_id = request.GET.get('id')

        person = request.user.person
        if customer_id:
            person = self.get_customer(customer_id).person

        serializer = serialize_created_lectures(request, person, from_attr=AttrNames.CUSTOMER)
        return lecture_responses.success_get_lectures(serializer.data)
