from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Min
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from chatapp.models import Chat, Message
from workroomsapp.lecture import lecture_responses
from workroomsapp.lecture.docs import lecture_docs
from workroomsapp.lecture.lecturer.lecture_as_lecturer_serializers import *
from workroomsapp.models import Respondent, LectureRequest, Lecturer, Customer
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
                lowest = lecture.lecture_requests.aggregate(minimum=Min('event__datetime_start'))
                lowest = lowest.get('minimum')
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


class PotentialLecturerLecturesGetAPIView(APIView):
    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        customers = Customer.objects.exclude(person__user=request.user)
        lecture_list = []
        for customer in customers:
            for lecture in customer.lectures.all():
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
        date = request.GET.get('date')

        if not lecture_id or not date:
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

        lecture_request = lecture.lecture_requests.filter(
            event__datetime_start=datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')).first()

        if not lecture_request:
            return lecture_responses.does_not_exist()

        if not lecture_request.respondents.filter(person=request.user.person).first():
            respondent = Respondent.objects.create(person=request.user.person)
            lecture_request.respondents.add(respondent)

            chat = Chat.objects.filter(users__in=[creator.user, request.user]).first()
            if not chat:
                chat = Chat.objects.create(lecture_request=lecture_request)
                chat.users.add(creator.user, request.user)
                chat.save()

            Message.objects.get_or_create(
                author=request.user,
                chat=chat,
                text='Добрый день! Мне подходит ваш запрос на проведение лекции!'
            )

            async_to_sync(channel_layer.group_send)(
                f'user_{creator.user.pk}',
                {
                    "type": "new_respondent",
                    "lecture_request": lecture_request,
                    "lecture_creator": creator.user,
                    "lecture_respondent": request.user
                }
            )

            async_to_sync(channel_layer.group_send)(
                f'user_{request.user.pk}',
                {
                    "type": "new_respondent",
                    "lecture_request": lecture_request,
                    "lecture_creator": creator.user,
                    "lecture_respondent": request.user
                }
            )

            lecture_request.save()
            return lecture_responses.success_response()
        else:
            Respondent.objects.get(person=request.user.person, lecture_requests=lecture_request).delete()
            chat = Chat.objects.filter(
                users__in=[creator.user, request.user]).first()

            async_to_sync(channel_layer.group_send)(
                f'user_{creator.user.pk}',
                {
                    "type": "remove_respondent",
                    "lecture_request": lecture_request,
                    "lecture_respondent": request.user
                }
            )

            if not chat:
                chat_list = Chat.objects.filter(lecture_request=lecture_request)
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

        if not lecture:
            return lecture_responses.lecture_does_not_exist()

        lecturer_lecture = None
        customer_lecture = None
        if request.user.person.is_lecturer:
            lecturer_lecture = request.user.person.lecturer.lecturer_lecture_requests.filter(
                lecture_request__lecture=lecture).first()
        elif request.user.person.is_customer:
            customer_lecture = request.user.person.customer.customer_lecture_requests.filter(
                lecture_request__lecture=lecture).first()

        if not lecturer_lecture and not customer_lecture:
            return lecture_responses.not_a_creator()

        respondent = lecture.lecture_request.respondents.filter(pk=respondent_id).first()

        if not respondent:
            return lecture_responses.not_a_respondent()

        if reject == 'true':
            respondent.delete()
            lecture.status = False
            lecture.save()
            async_to_sync(channel_layer.group_send)(
                f'user_{respondent.person.user.pk}',
                {
                    "type": "remove_respondent",
                    "lecture_request": lecture.lecture_request,
                    "lecture_respondent": respondent.person.user
                }
            )
            return lecture_responses.success_denied()

        respondent.confirmed = True
        lecture.status = True
        lecture.save()
        respondent.save()
        return lecture_responses.success_confirm()
