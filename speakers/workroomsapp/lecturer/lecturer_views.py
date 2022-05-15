from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from workroomsapp.lecturer.docs import lecturer_docs
from workroomsapp.lecturer.lecturer_serializers import *
from workroomsapp.utils import workroomsapp_permissions
from workroomsapp.lecturer import lecturer_responses


class DiplomaImageAPIView(APIView):
    permission_classes = [workroomsapp_permissions.IsLecturer]

    @swagger_auto_schema(**lecturer_docs.DiplomaImageCreateDoc)
    def post(self, request):
        serializer = DiplomaImageCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return lecturer_responses.photo_created()

    @swagger_auto_schema(**lecturer_docs.DiplomaImageGetDoc)
    def get(self, request):
        diploma_image = DiplomaImage.objects.filter(
            lecturer=request.user.person.lecturer
        ).first()

        if not diploma_image:
            return lecturer_responses.diploma_image_does_not_exist()

        serializer = DiplomaImageGetSerializer(
            diploma_image,
            context={'request': request})
        return lecturer_responses.success(serializer.data)


class LecturerCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(**lecturer_docs.LecturerCreateDoc)
    def post(self, request):
        serializer = LecturerCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return lecturer_responses.lecturer_created()
