from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from workroomsapp.models import LecturerCalendar
from workroomsapp.calendar.lecturer.lecturer_calendar_serializers import *
from workroomsapp.calendar.lecturer import lecturer_calendar_responses as responses
from workroomsapp.utils import workroomsapp_permissions


class LecturerCalendarAPIView(APIView):
    permission_classes = [workroomsapp_permissions.IsLecturer]

    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        lecturer_calendar = LecturerCalendar.objects.filter(lecturer=request.user.person.lecturer).first()

        if not lecturer_calendar:
            return responses.does_not_exist()

        serializer = LecturerCalendarSerializer(
            lecturer_calendar,
            context={'request': request}
        )

        return responses.success(serializer.data['calendar'])


class LecturerCalendarResponsesAPIView(APIView):
    permission_classes = [workroomsapp_permissions.IsLecturer]

    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        lecturer_calendar = LecturerCalendar.objects.filter(lecturer=request.user.person.lecturer).first()

        if not lecturer_calendar:
            return responses.does_not_exist()

        serializer = LecturerCalendarResponsesSerializer(
            lecturer_calendar,
            context={'request': request}
        )

        return responses.success(serializer.data['calendar'])
