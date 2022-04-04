from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from workroomsapp.lecture import lecture_responses
from workroomsapp.lecture.customer.lecture_as_customer_serializers import *
from workroomsapp.lecture.docs import lecture_docs
from workroomsapp.models import LecturerLectureRequest
from workroomsapp.utils import workroomsapp_permissions


class LectureAsCustomerAPIView(APIView):
    permission_classes = [workroomsapp_permissions.IsCustomer]

    @swagger_auto_schema(deprecated=True)
    def post(self, request):
        serializer = LectureCreateAsCustomerSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return lecture_responses.lecture_created()

    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        lecturer_lectures = LecturerLectureRequest.objects.exclude(
            lecturer__person__user=request.user)

        serializer = LectureAsCustomerGetSerializer(
            lecturer_lectures, many=True, context={'request': request})

        return lecture_responses.success_get_lectures(serializer.data)
