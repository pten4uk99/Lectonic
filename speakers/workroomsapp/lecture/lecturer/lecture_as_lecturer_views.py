import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import transaction
from django.db.models import Max, Min
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from chatapp.models import Chat, Message
from workroomsapp.lecture import lecture_responses
from workroomsapp.lecture.docs import lecture_docs
from workroomsapp.lecture.lecturer.lecture_as_lecturer_serializers import *
from workroomsapp.lecture.utils.mixins import LectureResponseMixin
from workroomsapp.models import LectureRequest, Lecturer, Customer, Respondent, Person
from workroomsapp.utils import workroomsapp_permissions

channel_layer = get_channel_layer()
logger = logging.getLogger(__name__)


class LectureAsLecturerAPIView(APIView):
    permission_classes = [workroomsapp_permissions.IsLecturer |
                          workroomsapp_permissions.IsCustomer]

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
        lecturer_id = request.GET.get('id')
        created_lectures = []

        if not lecturer_id:
            if hasattr(request.user.person, 'lecturer'):
                created_lectures = request.user.person.lecturer.lectures.all()
        else:
            created_lectures = Lecturer.objects.get(pk=lecturer_id).lectures.all()

        lectures_list = []
        for lecture in created_lectures:
            lowest = lecture.lecture_requests.aggregate(maximum=Max('event__datetime_start'))
            lowest = lowest.get('maximum')
            if lowest > datetime.datetime.now(tz=datetime.timezone.utc):
                lectures_list.append(lecture)

        serializer = LecturesGetSerializer(
            lectures_list, many=True, context={'request': request})

        return lecture_responses.success_get_lectures(serializer.data)

    @swagger_auto_schema(deprecated=True)
    def delete(self, request):
        lecture_id = request.GET.get('lecture_id')

        if not lecture_id:
            lecture_responses.not_in_data()

        lecture = Lecture.objects.filter(pk=lecture_id).first()

        if not lecture:
            return lecture_responses.does_not_exist()

        if lecture.lecturer:
            if not lecture.lecturer.person.user == request.user:
                return lecture_responses.not_a_creator()
        elif lecture.customer:
            if not lecture.customer.person.user == request.user:
                return lecture_responses.not_a_creator()

        lecture.delete()
        return lecture_responses.lecture_deleted()


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


class LecturesHistoryGetAPIView(APIView):
    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        query_from = request.GET.get('query_from')
        person = request.user.person
        created_lectures = getattr(person, query_from).lectures.all()

        lectures_list = []
        for lecture in created_lectures:
            aggregate = lecture.lecture_requests.aggregate(min=Min('event__datetime_start'))
            minimum = aggregate.get('min')

            if (minimum < datetime.datetime.now(tz=datetime.timezone.utc) and
                    lecture.lecture_requests.filter(respondent__confirmed=True)):
                lectures_list.append(lecture)

        serializer = LecturesGetSerializer(
            lectures_list, many=True, context={'request': request})

        return lecture_responses.success_get_lectures(serializer.data)


class ConfirmedLecturesGetAPIView(APIView):
    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        obj_name = request.GET.get('obj_name')

        respondents = Respondent.objects.filter(
            person=request.user.person,
            confirmed=True,
            lecture_request__event__datetime_start__gte=datetime.datetime.now(tz=datetime.timezone.utc))

        lecture_list = []
        for respondent in respondents:
            lecture = respondent.lecture_request.lecture
            if getattr(lecture, obj_name):
                lecture_list.append(respondent.lecture_request.lecture)

        serializer = LecturesGetSerializer(
            lecture_list, many=True, context={'request': request})

        return lecture_responses.success_get_lectures(serializer.data)


class PotentialLecturerLecturesGetAPIView(APIView):
    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        customers = Customer.objects.exclude(person__user=request.user)
        lecture_list = []
        for customer in customers:
            for lecture in customer.lectures.all():
                if lecture.lecture_requests.filter(respondent__confirmed=True):
                    continue
                lowest = lecture.lecture_requests.aggregate(maximum=Max('event__datetime_start'))
                lowest = lowest.get('maximum')
                if lowest > datetime.datetime.now(tz=datetime.timezone.utc):
                    lecture_list.append(lecture)

        serializer = LecturesGetSerializer(
            lecture_list, many=True, context={'request': request})

        return lecture_responses.success_get_lectures(serializer.data)


class LectureResponseAPIView(APIView, LectureResponseMixin):
    permission_classes = [workroomsapp_permissions.IsLecturer |
                          workroomsapp_permissions.IsCustomer]

    # проверить =>
    def add_respondent(self):
        for response_request in self.get_responses():
            response_request.respondents.add(self.request.user.person)
            response_request.save()
        logger.info(f'responses: {self.get_responses()}')

    def get_or_create_chat(self):
        responses = self.get_responses()
        chat = Chat.objects.filter(lecture_requests__in=responses).first()

        if not chat:
            chat = Chat.objects.create(lecture=self.get_lecture())
            chat.lecture_requests.add(*responses)
            chat.users.add(self.get_creator().user, self.request.user)
            chat.save()
        logger.info(f'users: {chat.users.all()}')
        return chat

    def create_response_message(self):
        dates = []
        for date in self.get_format_dates():
            dates.append(date.strftime('%d.%m'))

        message = Message.objects.create(
            author=self.request.user,
            chat=self.get_or_create_chat(),
            text=f'Собеседник заинтересован в Вашем предложении. '
                 f'Возможные даты проведения: {", ".join(dates)}.'
        )
        logger.info(f'text:{message.text}, author: {message.author}')

    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        with transaction.atomic():
            self.check_can_response(cancel=False)
            self.add_respondent()
            self.get_or_create_chat()
            self.create_response_message()
        return lecture_responses.success_response()


class LectureCancelResponseAPIView(APIView, LectureResponseMixin):
    permission_classes = [workroomsapp_permissions.IsLecturer |
                          workroomsapp_permissions.IsCustomer]

    # доделать и проверить =>
    def remove_respondent(self):
        for lecture_request in self.get_lecture().lecture_requests.all():
            respondent_obj = lecture_request.respondent.filter(person=self.request.user.person).first()

            if respondent_obj and not respondent_obj.rejected:
                lecture_request.respondents.remove(self.request.user.person)
                lecture_request.save()

    def remove_chat(self):
        chat = Chat.objects.filter(lecture_requests__in=self.get_responses()).first()

        if not chat:
            chat_list = Chat.objects.filter(lecture=self.get_lecture())
            for elem in chat_list:
                if elem.users.all().count() < 2:
                    elem.delete()
            # тут надо заменить return, думаю через вебсокет делать. Потому что скорее всего будет ошибка,
            # если тут он будет возвращать объект Response
            return lecture_responses.success_cancel([{'type': 'chat_does_not_exist'}])

        chat_id = chat.pk
        chat.delete()
        return chat_id

    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        with transaction.atomic():
            self.check_can_response(cancel=True)
            self.remove_respondent()
            chat_id = self.remove_chat()

        # тут возможно тоже из-за веб сокета такой ответ будет не нужен
        return lecture_responses.success_cancel([{
            'type': 'remove_respondent',
            'id': chat_id
        }])


class LectureToggleConfirmRespondentAPIView(APIView):
    @swagger_auto_schema(deprecated=True)
    def get(self, request):

        # переписать код как при отклике на лекцию

        lecture_id = request.GET.get('lecture')
        respondent_id = request.GET.get('respondent')
        chat_id = request.GET.get('chat_id')
        reject = request.GET.get('reject')

        if not lecture_id or not respondent_id or not chat_id:
            return lecture_responses.not_in_data()

        lecture = Lecture.objects.filter(pk=lecture_id).first()
        respondent = Person.objects.get(pk=respondent_id)
        chat = Chat.objects.get(pk=chat_id)

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

        lecture_requests = lecture.lecture_requests.filter(chat_list=chat)

        if not lecture_requests:
            return lecture_responses.not_a_respondent()

        chat_consumer_data = {
            "type": "chat_message",
            'author': request.user.pk,
            'text': '',
            'confirm': True
        }

        if reject == 'true':
            for lecture_request in lecture_requests:
                respondent_obj = Respondent.objects.get(lecture_request=lecture_request, person=respondent)
                respondent_obj.rejected = True
                respondent_obj.save()
            lecture.save()

            chat_consumer_data['confirm'] = False
            # async_to_sync(channel_layer.group_send)(f'chat_{chat.pk}', chat_consumer_data)
            # async_to_sync(channel_layer.group_send)(
            #     f'user_{respondent.user.pk}',
            #     {'type': 'new_message', 'chat_id': chat.pk}
            # )
            Message.objects.create(
                author=request.user,
                chat=chat,
                text=chat_consumer_data['text'],
                confirm=chat_consumer_data.get('confirm')
            )
            return lecture_responses.success_denied()

        for lecture_request in lecture_requests:
            lecture_respondent = Respondent.objects.get(person=respondent, lecture_request=lecture_request)
            lecture_respondent.confirmed = True
            lecture_respondent.save()
        lecture.save()

        Message.objects.create(
            author=request.user,
            chat=chat,
            text=chat_consumer_data['text'],
            confirm=chat_consumer_data.get('confirm')
        )

        # async_to_sync(channel_layer.group_send)(f'chat_{chat.pk}', chat_consumer_data)
        # async_to_sync(channel_layer.group_send)(
        #     f'user_{respondent.user.pk}',
        #     {'type': 'new_message', 'chat_id': chat.pk}
        # )
        return lecture_responses.success_confirm()
