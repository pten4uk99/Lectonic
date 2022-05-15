from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from workroomsapp.calendar.customer.customer_calendar_serializers import *
from workroomsapp.models import CustomerCalendar
from workroomsapp.calendar.customer import customer_calendar_responses as responses
from workroomsapp.utils import workroomsapp_permissions


class CustomerCalendarAPIView(APIView):
    permission_classes = [workroomsapp_permissions.IsCustomer]

    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        customer_calendar = CustomerCalendar.objects.filter(customer=request.user.person.customer).first()

        if not customer_calendar:
            return responses.does_not_exist()

        serializer = CustomerCalendarSerializer(
            customer_calendar,
            context={'request': request}
        )

        return responses.success(serializer.data['calendar'])


class CustomerCalendarResponsesAPIView(APIView):
    permission_classes = [workroomsapp_permissions.IsCustomer]

    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        customer_calendar = CustomerCalendar.objects.filter(customer=request.user.person.customer).first()

        if not customer_calendar:
            return responses.does_not_exist()

        serializer = CustomerCalendarResponsesSerializer(
            customer_calendar,
            context={'request': request}
        )

        return responses.success(serializer.data['calendar'])
