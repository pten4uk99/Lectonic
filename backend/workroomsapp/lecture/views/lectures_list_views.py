from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from workroomsapp.lecture import lecture_responses
from services.api import serialize_confirmed_lectures, serialize_potential_lectures
from services import AttrNames


class ConfirmedLecturesGetAPIView(APIView):
    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        # чьи лекции берем
        obj_name = self.request.GET.get('obj_name')
        # от кого идет запрос
        query_from = AttrNames.LECTURER if obj_name == AttrNames.CUSTOMER.value else AttrNames.CUSTOMER

        serializer = serialize_confirmed_lectures(from_obj=request.user, from_attr=query_from)
        return lecture_responses.success_get_lectures(serializer.data)


class PotentialLecturerLecturesGetAPIView(APIView):
    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        serializer = serialize_potential_lectures(from_obj=request.user, from_attr=AttrNames.LECTURER)
        return lecture_responses.success_get_lectures(serializer.data)


class PotentialCustomerLecturesGetAPIView(APIView):
    @swagger_auto_schema(deprecated=True)
    def get(self, request):
        serializer = serialize_potential_lectures(from_obj=request.user, from_attr=AttrNames.CUSTOMER)
        return lecture_responses.success_get_lectures(serializer.data)

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
#         if params.get('person_id_type'):
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
#             if (minimum < datetime.datetime.now() and
#                     lecture.lecture_requests.filter(respondent_obj__confirmed=True)):
#                 lectures_list.append(lecture)
#
#         return lectures_list
#
#
# class LecturesHistoryGetAPIView(LecturesGetAPIView, LecturesHistoryMixin):
#     """ Основной класс для связи с роутами, который строится из двух базовых классов """
#     pass
