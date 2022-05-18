import datetime

from django.urls import reverse
from workroomsapp.lecture.tests.base import get_str_range_datetime, BaseLectureAsCustomerCreateTestCase


# class TestCustomerCalendarGet(BaseLectureAsCustomerCreateTestCase):
#     def setUp(self):
#         super().setUp()
#         for i in range(7):
#             temp_data = self.lecture_data.copy()
#             temp_data['name'] = f'Моя лектушка {i}'
#             temp_data['datetime'] = [
#                 get_str_range_datetime(now_plus=datetime.timedelta(days=2 + i),
#                                        end_plus=datetime.timedelta(days=2 + i, hours=1))
#             ]
#             r = self.make_request(temp_data)
#
#     def test_get_calendar(self):
#         response = self.client.get(
#             reverse('customer_calendar'), {'year': datetime.datetime.now().year,
#                                            'month': datetime.datetime.now().month})
#         # Если уже конец месяца, то события могут отображаться некорректно
#         self.assertEqual(
#             'data' in response.data and type(response.data['data']) == list, True,
#             msg='В ответе нет списка data'
#         )
#         self.assertEqual(
#             'date' in response.data['data'][0], True,
#             msg='В словаре списка data нет ключа date'
#         )
#         self.assertEqual(
#             len(response.data['data'][0]['events']), 1,
#             msg='Неверное количество событий'
#         )
#         self.assertEqual(
#             len(response.data['data'][1]['events']), 1,
#             msg='Неверное количество событий'
#         )
#         self.assertEqual(
#             len(response.data['data'][2]['events']), 2,
#             msg='Неверное количество событий'
#         )
