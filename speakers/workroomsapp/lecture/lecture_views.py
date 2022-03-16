from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from workroomsapp.lecture import lecture_responses
from workroomsapp.lecture.docs import lecture_docs
from workroomsapp.lecture.lecture_serializers import *
from workroomsapp.utils import workroomsapp_permissions


class LectureAsLecturerAPIView(APIView):
    permission_classes = [workroomsapp_permissions.IsLecturer]

    @swagger_auto_schema(**lecture_docs.LectureAsLecturerCreateDoc)
    def post(self, request):
        print(request.data)
        serializer = LectureCreateAsLecturerSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return lecture_responses.lecture_as_lecturer_created()
