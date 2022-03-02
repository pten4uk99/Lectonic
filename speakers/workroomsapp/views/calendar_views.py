from rest_framework.response import Response
from rest_framework.views import APIView

from workroomsapp.models import LecturerCalendar, Lecturer
from workroomsapp.serializers.calendar_serializers import LecturerCalendarSerializer
from workroomsapp.utils import workroomsapp_permissions
from workroomsapp.utils.responses import calendar_responses as responses


class LecturerCalendarAPIView(APIView):
    # permission_classes = [workroomsapp_permissions.IsLecturer]

    def get(self, request):
        lecturer_calendar = LecturerCalendar.objects.filter(lecturer=request.user.lecturer)

        if not lecturer_calendar:
            return responses.does_not_exist()

        serializer = LecturerCalendarSerializer(
            lecturer_calendar,
            context={'request': request}
        )

        return responses.success(serializer.data['calendar'])
