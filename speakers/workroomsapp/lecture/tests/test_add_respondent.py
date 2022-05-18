from django.urls import reverse

from authapp.models import User
from speakers.utils.tests import data
from workroomsapp.lecture.tests.base import BaseLectureAsCustomerCreateTestCase
from workroomsapp.models import *


class AddRespondent(BaseLectureAsCustomerCreateTestCase):
    signup_data2 = data.SIGNUP.copy()
    lecturer_lecture_data = data.LECTURE.copy()

    def setUp(self):
        super().setUp()
        user = User.objects.create(**self.signup_data2)
        self.profile_data['user'] = user
        self.profile_data['city'] = City.objects.get(pk=1)
        person = Person.objects.create(**self.profile_data)
        Lecturer.objects.create_lecturer(**self.lecturer_data, person=person)

    def test_add_respondent(self):
        self.client.logout()
        self.client.post(reverse('login'), self.signup_data2)
        self.client.post(reverse('lecture_as_lecturer'), self.lecturer_lecture_data)
        self.client.logout()
        self.client.post(reverse('login'), self.signup_data)
        event = Lecture.objects.first().lecture_requests.first().event
        response = self.client.get(
            reverse('lecture_response'),
            {
                'lecture': Lecture.objects.first().pk,
                'date': [event.datetime_start.strftime('%Y-%m-%dT%H:%M')]
            }
        )

        self.assertEqual(
            Lecture.objects.first().lecture_requests.first().respondents.all().exists(),
            True,
            msg='Пользователь не был добавлен в откликнувшиеся на лекцию\n'
                f'Ответ: {response.data}'
        )

