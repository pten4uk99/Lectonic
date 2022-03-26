from rest_framework.views import APIView

from workroomsapp.models import LecturerCalendar
from workroomsapp.calendar.lecturer.lecturer_calendar_serializers import LecturerCalendarSerializer
from workroomsapp.calendar.lecturer import lecturer_calendar_responses as responses
from workroomsapp.utils import workroomsapp_permissions


class LecturerCalendarAPIView(APIView):
    permission_classes = [workroomsapp_permissions.IsLecturer]

    def get(self, request):
        lecturer_calendar = LecturerCalendar.objects.filter(lecturer=request.user.person.lecturer).first()

        if not lecturer_calendar:
            return responses.does_not_exist()

        serializer = LecturerCalendarSerializer(
            lecturer_calendar,
            context={'request': request}
        )

        return responses.success(serializer.data['calendar'])
