from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.views import APIView

from services.filters import CustomerFilter
from workroomsapp.customer import customer_responses
from workroomsapp.customer.customer_serializers import *
from workroomsapp.customer.docs import customer_docs
from workroomsapp.lecturer import lecturer_responses
from workroomsapp.lecturer.lecturer_serializers import LecturersListGetSerializer
from workroomsapp.models import Customer


class CustomerAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(**customer_docs.CustomerCreateDoc)
    def post(self, request):
        serializer = CustomerCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return customer_responses.customer_created()

    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        user_id = request.GET.get('user_id')

        customer = Customer.objects.filter(person__user_id=user_id)

        if not customer:
            return customer_responses.customer_does_not_exist()

        serializer = CustomerGetSerializer(customer, many=True, context={'request': request})
        return customer_responses.success_get_customer(serializer.data)


class CustomersListGetAPIView(APIView):
    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        city = request.GET.get('city', '')
        domain = request.GET.get('domain', '')

        filter_class = CustomerFilter(qs=Customer.objects.all(), from_obj=request.user, city=city, domain=domain)
        serializer = LecturersListGetSerializer(filter_class.filter(), many=True, context={'request': request})
        return lecturer_responses.success_get_lecturers(serializer.data)
