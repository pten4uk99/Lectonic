from django.urls import reverse
from rest_framework.test import APITestCase

from authapp.models import User
from workroomsapp.models import *


class TestLecturerCalendarGet(APITestCase):

    def setUp(self):
        signup_data = {'email': 'admin@admin.ru', 'password': '12345678'}
        self.client.post(reverse('signup'), signup_data)

        person = Person.objects.create(
            pk=1,
            user=User.objects.first(),
            first_name='Никита',
            last_name='Павленко',
            birth_date=datetime.datetime(2020, 2, 15),
            city=City.objects.create(name='Москва', pk=1),
            is_lecturer=True
        )
        lecturer = Lecturer.objects.create(pk=1, person=person)
        calendar = Calendar.objects.create()
        LecturerCalendar.objects.create(lecturer=lecturer, calendar=calendar)

        event1 = Event.objects.create(pk=1, datetime=datetime.datetime.now(tz=datetime.timezone.utc))
        event2 = Event.objects.create(
            pk=2,
            datetime=datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=2)
        )
        event3 = Event.objects.create(
            pk=3,
            datetime=datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(hours=2)
        )
        event4 = Event.objects.create(
            pk=4,
            datetime=datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=2)
        )

        lecture_request1 = LectureRequest.objects.create(
            lecture=Lecture.objects.create(name='Лекция1'), event=event1
        )
        lecture_request2 = LectureRequest.objects.create(
            lecture=Lecture.objects.create(name='Лекция2'), event=event2
        )
        lecture_request3 = LectureRequest.objects.create(
            lecture=Lecture.objects.create(name='Лекция3'), event=event3
        )
        lecture_request4 = LectureRequest.objects.create(
            lecture=Lecture.objects.create(name='Лекция4'), event=event4
        )

        LecturerLectureRequest.objects.create(lecture_request=lecture_request1, lecturer=lecturer)
        LecturerLectureRequest.objects.create(lecture_request=lecture_request2, lecturer=lecturer)
        LecturerLectureRequest.objects.create(lecture_request=lecture_request3, lecturer=lecturer)
        LecturerLectureRequest.objects.create(lecture_request=lecture_request4, lecturer=lecturer)

        calendar.events.add(event4, event3, event2, event1)
        calendar.save()



    def test_credentials(self):
        response = self.client.get(reverse('lecturer_calendar'), {'year': 2022, 'month': 2})
        print(response.data)
        # self.assertEqual(
        #     response.status_code, 401,
        #     msg='Неверный статус ответа при попытке получения города неавторизованного пользователя'
        # )