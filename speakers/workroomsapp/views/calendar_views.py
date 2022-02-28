from rest_framework.response import Response
from rest_framework.views import APIView

from workroomsapp.models import LecturerCalendar, Lecturer
from workroomsapp.serializers.calendar_serializers import LecturerCalendarSerializer
from workroomsapp.utils import workroomsapp_permissions


class LecturerCalendarAPIView(APIView):
    # permission_classes = [workroomsapp_permissions.IsLecturer]

    def get(self, request):
        serializer = LecturerCalendarSerializer(
            LecturerCalendar.objects.get(lecturer=Lecturer.objects.first()),
            context={'request': request}
        )

        return Response(data=serializer.data)
