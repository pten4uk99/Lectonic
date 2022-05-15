import datetime

from django.db.models import Min, Max
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from workroomsapp.lecture import lecture_responses
from workroomsapp.lecture.serializers.as_lecturer_serializers import LecturesGetSerializer
from workroomsapp.models import Customer, Person, Lecturer


class LecturesListBaseMixin:
    def get_params(self):
        """ Получает параметры из запроса и проверяет, все ли необходимые переданы """

        raise NotImplementedError()

    def filter_lectures(self):
        """ Базовый метод для фильтрации лекций """

        raise NotImplementedError()


class ConfirmedLecturesMixin(LecturesListBaseMixin):
    def get_params(self):
        obj_name = self.request.GET.get('obj_name')  # чьи лекции берем
        query_from = 'lecturer' if obj_name == 'customer' else 'customer'  # от кого идет запрос
        return {'obj_name': obj_name, 'query_from': query_from}

    def get_own_lectures(self):
        """ Возвращает список подтвержденных собственных лекций """

        query_from = self.get_params()['query_from']
        lecture_list = []

        lectures = getattr(self.request.user.person, query_from).lectures.filter(
            lecture_requests__respondent_obj__confirmed=True,
            lecture_requests__event__datetime_start__gte=datetime.datetime.now(tz=datetime.timezone.utc))

        for self_lecture in lectures:
            if getattr(self_lecture, query_from) and self_lecture not in lecture_list:
                lecture_list.append(self_lecture)

        return lecture_list

    def get_own_responses(self):
        """ Возвращает список подтвердженных лекций, на которые откликнулся пользователь """

        obj_name = self.get_params()['obj_name']
        lecture_list = []

        respondents = self.request.user.person.respondent_obj.filter(
            confirmed=True,
            lecture_request__event__datetime_start__gte=datetime.datetime.now(tz=datetime.timezone.utc))

        for respondent in respondents:
            lecture = respondent.lecture_request.lecture
            if getattr(lecture, obj_name) and lecture not in lecture_list:
                lecture_list.append(lecture)

        return lecture_list

    def filter_lectures(self):
        """ Возвращает список собственных подтвержденных лекций +
        список подтвержденных лекций, на которые откликнулся пользователь. """

        return self.get_own_responses() + self.get_own_lectures()


class PotentialLecturesMixin(LecturesListBaseMixin):
    def get_creators(self):
        """ Базовый метод для получения создателей лекций """

        raise NotImplementedError()

    def filter_lectures(self):
        creators = self.get_creators()
        lecture_list = []

        for creator in creators:
            for lecture in creator.lectures.all():

                if lecture.lecture_requests.filter(
                        respondent_obj__confirmed=True, respondent_obj__person=self.request.user.person):
                    continue

                lowest = lecture.lecture_requests.aggregate(maximum=Max('event__datetime_start'))
                lowest = lowest.get('maximum')

                if lowest > datetime.datetime.now(tz=datetime.timezone.utc):
                    lecture_list.append(lecture)

        return lecture_list


class LecturesGetAPIView(APIView):
    """ Базовый класс для обработки GET запроса """

    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        try:
            query_from = self.get_params().get('query_from')
        except NotImplementedError:
            query_from = None

        lectures_list = self.filter_lectures()
        serializer = LecturesGetSerializer(
            lectures_list,
            many=True,
            context={'request': request, 'query_from': query_from})

        return lecture_responses.success_get_lectures(serializer.data)


class ConfirmedLecturesGetAPIView(LecturesGetAPIView, ConfirmedLecturesMixin):
    """ Основной класс для связи с роутами, который строится из двух базовых классов """
    pass


class PotentialLecturerLecturesGetAPIView(LecturesGetAPIView, PotentialLecturesMixin):
    """ Основной класс для связи с роутами, который строится из двух базовых классов """

    def get_creators(self):
        return Customer.objects.exclude(person__user=self.request.user)


class PotentialCustomerLecturesGetAPIView(LecturesGetAPIView, PotentialLecturesMixin):
    """ Основной класс для связи с роутами, который строится из двух базовых классов """

    def get_creators(self):
        return Lecturer.objects.exclude(person__user=self.request.user)


# class LecturesHistoryMixin(LecturesListBaseMixin):
#     def get_params(self):
#         query_from = self.request.GET.get('query_from')
#         obj_id = self.request.GET.get('id')
#
#         return {'query_from': query_from, 'obj_id': obj_id}
#
#     def get_created_lectures(self):
#         """ Проверяет действительно ли у данного пользователя есть выбранная роль,
#         и, если это так, то возвращает список созданных лекций. """
#
#         params = self.get_params()
#
#         if params.get('person_id'):
#             if params['query_from'] == 'lecturer':
#                 person = Lecturer.objects.get(pk=params['obj_id']).person
#             else:
#                 person = Customer.objects.get(pk=params['obj_id']).person
#         else:
#             person = self.request.user.person
#
#         lectures_creator = getattr(
#             person, self.get_params()['query_from'], None)
#
#         if not lectures_creator:
#             return lecture_responses.not_a_creator()
#
#         created_lectures = lectures_creator.lectures.all()
#
#         return created_lectures
#
#     def filter_lectures(self):
#         created_lectures = self.get_created_lectures()
#         lectures_list = []
#
#         for lecture in created_lectures:
#             aggregate = lecture.lecture_requests.aggregate(min=Min('event__datetime_start'))
#             minimum = aggregate.get('min')
#
#             if (minimum < datetime.datetime.now(tz=datetime.timezone.utc) and
#                     lecture.lecture_requests.filter(respondent_obj__confirmed=True)):
#                 lectures_list.append(lecture)
#
#         return lectures_list
#
#
# class LecturesHistoryGetAPIView(LecturesGetAPIView, LecturesHistoryMixin):
#     """ Основной класс для связи с роутами, который строится из двух базовых классов """
#     pass
