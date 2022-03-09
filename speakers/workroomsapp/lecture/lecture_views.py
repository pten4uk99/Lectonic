from rest_framework.views import APIView

from workroomsapp.lecture import lecture_responses
from workroomsapp.lecture.lecture_serializers import *


class LectureAPIView(APIView):
    def post(self, request):
        serializer = LectureCreateAsLecturerSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return lecture_responses.lecture_as_lecturer_created()