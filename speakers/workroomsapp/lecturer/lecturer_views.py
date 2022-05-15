from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from workroomsapp.lecturer.docs import lecturer_docs
from workroomsapp.lecturer.lecturer_serializers import *
from workroomsapp.models import City
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

    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        lecturer_id = request.GET.get('id')

        lecturer = Lecturer.objects.filter(pk=lecturer_id)

        if not lecturer:
            return lecturer_responses.lecturer_does_not_exist()

        serializer = LecturerGetSerializer(lecturer, many=True, context={'request': request})
        city_id = serializer.data[0]['person']['city']
        serializer.data[0]['person']['city'] = City.objects.get(pk=city_id).name
        return lecturer_responses.success_get_lecturers(serializer.data)


class LecturersListGetAPIView(APIView):
    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        lecturers = Lecturer.objects.exclude(person__user=request.user)

        serializer = LecturersListGetSerializer(
            lecturers, many=True, context={'request': request})

        return lecturer_responses.success_get_lecturers(serializer.data)
