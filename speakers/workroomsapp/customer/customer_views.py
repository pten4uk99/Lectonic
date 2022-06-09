from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.views import APIView

from workroomsapp.customer.customer_serializers import *
from workroomsapp.customer import customer_responses
from workroomsapp.customer.docs import customer_docs
from workroomsapp.models import Customer, City


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
        customer_id = request.GET.get('id')

        customer = Customer.objects.filter(pk=customer_id)

        if not customer:
            return customer_responses.customer_does_not_exist()

        serializer = CustomerGetSerializer(customer, many=True, context={'request': request})
        return customer_responses.success_get_customer(serializer.data)

