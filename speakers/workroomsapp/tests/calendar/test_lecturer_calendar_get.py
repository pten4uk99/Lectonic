import datetime

from django.urls import reverse
from rest_framework.test import APITestCase

from authapp.models import User
from workroomsapp.models import *


# class TestLecturerCalendarGet(APITestCase):
#
#     def setUp(self):
#         signup_data = {'email': 'admin@admin.ru', 'password': '12345678'}
#         self.client.post(reverse('signup'), signup_data)
#
#         person = Person.objects.create(
#             pk=1,
#             user=User.objects.first(),
#             first_name='Никита',
#             last_name='Павленко',
#             birth_date=datetime.datetime(2020, 2, 15),
#             city=City.objects.create(name='Москва', pk=1),
#             is_lecturer=True
#         )
#         lecturer = Lecturer.objects.create_lecturer(person=person)
#
#         Lecture.objects.create_as_lecturer(
#             name='Моя лектушка',
#             lecturer=lecturer,
#             datetime=datetime.datetime.now(tz=datetime.timezone.utc)
#         )
#         Lecture.objects.create_as_lecturer(
#             name='Твоя лектушка',
#             lecturer=lecturer,
#             datetime=datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=2)
#         )
#         Lecture.objects.create_as_lecturer(
#             name='Его лектушка',
#             lecturer=lecturer,
#             datetime=datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(hours=2)
#         )
#         Lecture.objects.create_as_lecturer(
#             name='Ее лектушка',
#             lecturer=lecturer,
#             datetime=datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=2)
#         )
#
#     def test_get_calendar(self):
#         response = self.client.get(reverse('lecturer_calendar'), {'year': 2022, 'month': 3})
#         print(response.data)
#         self.assertEqual(
#             'data' in response.data and type(response.data['data']) == list, True,
#             msg='В ответе нет списка data'
#         )
#         self.assertEqual(
#             'date' in response.data['data'][0], True,
#             msg='В словаре списка data нет ключа date'
#         )
#         self.assertEqual(
#             len(response.data['data'][0]['events']), 4,
#             msg='Неверное количество событий'
#         )
