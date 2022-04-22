from django.db.models import Max
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from workroomsapp.lecture import lecture_responses
from workroomsapp.lecture.customer.lecture_as_customer_serializers import *
from workroomsapp.lecture.docs import lecture_docs
from workroomsapp.lecture.lecturer.lecture_as_lecturer_serializers import LecturesGetSerializer
from workroomsapp.models import LectureRequest, Customer, Lecturer, Respondent
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
        customer_id = request.GET.get('id')
        created_lectures = []

        if not customer_id:
            if hasattr(request.user.person, 'customer'):
                created_lectures = request.user.person.customer.lectures.all()
        else:
            created_lectures = Customer.objects.get(pk=customer_id).lectures.all()

        lectures_list = []
        for lecture in created_lectures:
            lowest = lecture.lecture_requests.aggregate(maximum=Max('event__datetime_start'))
            lowest = lowest.get('maximum')
            if lowest > datetime.datetime.now(tz=datetime.timezone.utc):
                lectures_list.append(lecture)

        serializer = LecturesGetSerializer(
            lectures_list, many=True, context={'request': request})

        return lecture_responses.success_get_lectures(serializer.data)


class PotentialCustomerLecturesGetAPIView(APIView):
    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        lecturers = Lecturer.objects.exclude(person__user=request.user)
        lecture_list = []
        for lecturer in lecturers:
            for lecture in lecturer.lectures.all():
                if lecture.lecture_requests.filter(respondent__confirmed=True):
                    continue
                lowest = lecture.lecture_requests.aggregate(maximum=Max('event__datetime_start'))
                lowest = lowest.get('maximum')
                if lowest > datetime.datetime.now(tz=datetime.timezone.utc):
                    lecture_list.append(lecture)

        serializer = LecturesGetSerializer(
            lecture_list, many=True, context={'request': request})

        return lecture_responses.success_get_lectures(serializer.data)

