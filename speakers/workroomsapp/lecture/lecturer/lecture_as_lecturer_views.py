from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Max
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from chatapp.models import Chat, Message
from workroomsapp.lecture import lecture_responses
from workroomsapp.lecture.docs import lecture_docs
from workroomsapp.lecture.lecturer.lecture_as_lecturer_serializers import *
from workroomsapp.models import LectureRequest, Lecturer, Customer
from workroomsapp.utils import workroomsapp_permissions

channel_layer = get_channel_layer()


class LectureAsLecturerAPIView(APIView):
    permission_classes = [workroomsapp_permissions.IsLecturer]

    @swagger_auto_schema(**lecture_docs.LectureAsLecturerCreateDoc)
    def post(self, request):
        serializer = LectureCreateAsLecturerSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return lecture_responses.lecture_created()

    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        lectures_list = None

        if hasattr(request.user.person, 'lecturer'):
            created_lectures = request.user.person.lecturer.lectures.all()
            lectures_list = []
            for lecture in created_lectures:
                lowest = lecture.lecture_requests.aggregate(maximum=Max('event__datetime_start'))
                lowest = lowest.get('maximum')
                if lowest > datetime.datetime.now(tz=datetime.timezone.utc):
                    lectures_list.append(lecture)


        serializer = LecturesGetSerializer(
            lectures_list, many=True, context={'request': request})

        return lecture_responses.success_get_lectures(serializer.data)


class LectureDetailAPIView(APIView):
    @swagger_auto_schema(deprecated=True)
    def get(self, request, pk):
        if not pk:
            return lecture_responses.not_in_data()

        lecture = Lecture.objects.filter(pk=pk)

        if not lecture.first():
            return lecture_responses.does_not_exist()

        serializer = LecturesGetSerializer(
            lecture, many=True, context={'request': request})

        return lecture_responses.success_get_lectures(serializer.data)


class LecturerLecturesHistoryGetAPIView(APIView):
    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        lectures_list = None

        if hasattr(request.user.person, 'lecturer'):
            created_lectures = request.user.person.lecturer.lectures.all()
            lectures_list = []
            for lecture in created_lectures:
                biggest = lecture.lecture_requests.aggregate(maximum=Max('event__datetime_start'))
                biggest = biggest.get('maximum')
                if biggest < datetime.datetime.now(tz=datetime.timezone.utc) and lecture.confirmed_person:
                    lectures_list.append(lecture)

        serializer = LecturesGetSerializer(
            lectures_list, many=True, context={'request': request})

        return lecture_responses.success_get_lectures(serializer.data)


class PotentialLecturerLecturesGetAPIView(APIView):
    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        customers = Customer.objects.exclude(person__user=request.user)
        lecture_list = []
        for customer in customers:
            for lecture in customer.lectures.all():
                lowest = lecture.lecture_requests.aggregate(maximum=Max('event__datetime_start'))
                lowest = lowest.get('maximum')
                if lowest > datetime.datetime.now(tz=datetime.timezone.utc):
                    lecture_list.append(lecture)

        serializer = LecturesGetSerializer(
            lecture_list, many=True, context={'request': request})

        return lecture_responses.success_get_lectures(serializer.data)


class LectureResponseAPIView(APIView):
    permission_classes = [workroomsapp_permissions.IsLecturer |
                          workroomsapp_permissions.IsCustomer]

    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        lecture_id = request.GET.get('lecture')
        dates = request.GET.getlist('date')

        if not lecture_id:
            return lecture_responses.not_in_data()

        lecture = Lecture.objects.filter(pk=lecture_id).first()
        creator = None

        if not lecture:
            return lecture_responses.lecture_does_not_exist()

        if not lecture.customer:
            if not hasattr(request.user.person, 'customer'):
                return lecture_responses.lecturer_forbidden()
        else:
            creator = lecture.customer.person

        if not lecture.lecturer:
            if not hasattr(request.user.person, 'lecturer'):
                return lecture_responses.customer_forbidden()
        else:
            creator = lecture.lecturer.person

        lecture_requests = lecture.lecture_requests.all()

        if not lecture_requests:
            return lecture_responses.does_not_exist()

        if not lecture_requests.filter(respondents=request.user.person).first():
            if not dates:
                return lecture_responses.not_in_data()

            format_dates = []
            for date in dates:
                format_dates.append(datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M'))

            response_lecture_requests = lecture_requests.filter(event__datetime_start__in=format_dates)

            if not response_lecture_requests:
                return lecture_responses.does_not_exist()

            for response_request in response_lecture_requests:
                response_request.respondents.add(request.user.person)
                response_request.save()

            chat = Chat.objects.filter(users__in=[creator.user, request.user]).first()
            if not chat:
                chat = Chat.objects.create(lecture=lecture)
                chat.users.add(creator.user, request.user)
                chat.save()

            async_to_sync(channel_layer.group_send)(
                f'user_{creator.user.pk}',
                {
                    "type": "new_respondent",
                    "dates": format_dates,
                    "lecture": lecture,
                    "lecture_creator": creator.user,
                    "lecture_respondent": request.user
                }
            )

            async_to_sync(channel_layer.group_send)(
                f'user_{request.user.pk}',
                {
                    "type": "new_respondent",
                    "dates": format_dates,
                    "lecture": lecture,
                    "lecture_creator": creator.user,
                    "lecture_respondent": request.user
                }
            )

            lecture.save()
            return lecture_responses.success_response()
        else:
            for lecture_request in lecture_requests:
                lecture_request.respondents.remove(request.user.person)
                lecture_request.save()
            chat = Chat.objects.filter(users__in=[creator.user, request.user]).first()

            async_to_sync(channel_layer.group_send)(
                f'user_{creator.user.pk}',
                {
                    "type": "remove_respondent",
                    "lecture": lecture,
                    "lecture_respondent": request.user
                }
            )

            if not chat:
                chat_list = Chat.objects.filter(lecture=lecture)
                for elem in chat_list:
                    if elem.users.all().count() < 2:
                        elem.delete()
                return lecture_responses.success_cancel([{'type': 'chat_does_not_exist'}])
            return lecture_responses.success_cancel([{
                'type': 'remove_respondent',
                'id': chat.pk
            }])


class LectureToggleConfirmRespondentAPIView(APIView):
    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        lecture_id = request.GET.get('lecture')
        respondent_id = request.GET.get('respondent')
        reject = request.GET.get('reject')

        if not lecture_id or not respondent_id:
            return lecture_responses.not_in_data()

        lecture = Lecture.objects.filter(pk=lecture_id).first()
        respondent = Person.objects.get(pk=respondent_id)

        if not lecture:
            return lecture_responses.lecture_does_not_exist()

        is_lecturer = False
        is_customer = False

        if lecture.lecturer:
            is_lecturer = lecture.lecturer.person.user == request.user
        elif lecture.customer:
            is_customer = lecture.customer.person.user == request.user

        if not is_lecturer and not is_customer:
            return lecture_responses.not_a_creator()

        lecture_requests = lecture.lecture_requests.filter(respondents=respondent)

        if not lecture_requests:
            return lecture_responses.not_a_respondent()


        if reject == 'true':
            for lecture_request in lecture_requests:
                lecture_request.respondents.remove(respondent)
                lecture_request.save()
            lecture.confirmed_person = None
            lecture.status = False
            lecture.save()
            async_to_sync(channel_layer.group_send)(
                f'user_{respondent.user.pk}',
                {
                    "type": "remove_respondent",
                    "lecture": lecture,
                    "lecture_respondent": respondent.user
                }
            )
            return lecture_responses.success_denied()

        lecture.confirmed_person = respondent
        lecture.status = True
        lecture.save()
        respondent.save()
        return lecture_responses.success_confirm()
