from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from workroomsapp.lecture import lecture_responses
from workroomsapp.lecture.customer.lecture_as_customer_serializers import *
from workroomsapp.lecture.docs import lecture_docs
from workroomsapp.lecture.lecturer.lecture_as_lecturer_serializers import LecturesGetSerializer
from workroomsapp.models import LectureRequest, Customer, Lecturer
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
        created_lectures = None

        if hasattr(request.user.person, 'customer'):
            created_lectures = request.user.person.customer.lectures.all()

        serializer = LecturesGetSerializer(
            created_lectures, many=True, context={'request': request})

        return lecture_responses.success_get_lectures(serializer.data)


class PotentialCustomerLecturesGetAPIView(APIView):
    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        lecturers = Lecturer.objects.exclude(person__user=request.user)
        lecture_list = []
        for lecturer in lecturers:
            for lecture in lecturer.lectures.all():
                lecture_list.append(lecture)

        serializer = LecturesGetSerializer(
            lecture_list, many=True, context={'request': request})

        return lecture_responses.success_get_lectures(serializer.data)
