from django.db.models import Max
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from workroomsapp.lecture import lecture_responses
from workroomsapp.lecture.serializers.as_lecturer_serializers import *
from workroomsapp.models import Customer, Lecturer
from workroomsapp.utils import workroomsapp_permissions


class LectureAsCustomerAPIView(APIView):
    permission_classes = [workroomsapp_permissions.IsCustomer]

    def get_all_lectures(self):
        customer_id = self.request.GET.get('id')
        created_lectures = []

        if not customer_id:
            if hasattr(self.request.user.person, 'customer'):
                created_lectures = self.request.user.person.customer.lectures.all()
        else:
            created_lectures = Customer.objects.get(pk=customer_id).lectures.all()
        return created_lectures

    def filter_lectures(self):
        lectures = self.get_all_lectures()
        filtered_lectures = []

        for lecture in lectures:
            lowest = lecture.lecture_requests.aggregate(maximum=Max('event__datetime_start'))
            lowest = lowest.get('maximum')

            if lowest > datetime.datetime.now(tz=datetime.timezone.utc):
                filtered_lectures.append(lecture)

        return filtered_lectures

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
        serializer = LecturesGetSerializer(
            self.filter_lectures(),
            many=True,
            context={'request': request}
        )
        return lecture_responses.success_get_lectures(serializer.data)
