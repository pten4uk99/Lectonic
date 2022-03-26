from rest_framework.views import APIView

from workroomsapp.calendar.customer.customer_calendar_serializers import CustomerCalendarSerializer
from workroomsapp.models import CustomerCalendar
from workroomsapp.calendar.lecturer import lecturer_calendar_responses as responses
from workroomsapp.utils import workroomsapp_permissions


class CustomerCalendarAPIView(APIView):
    permission_classes = [workroomsapp_permissions.IsCustomer]

    def get(self, request):
        customer_calendar = CustomerCalendar.objects.filter(customer=request.user.person.customer).first()

        if not customer_calendar:
            return responses.does_not_exist()

        serializer = CustomerCalendarSerializer(
            customer_calendar,
            context={'request': request}
        )

        return responses.success(serializer.data['calendar'])
