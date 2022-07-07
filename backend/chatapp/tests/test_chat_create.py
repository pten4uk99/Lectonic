import datetime

from django.urls import reverse
from rest_framework.test import APITestCase

from authapp.models import User
from chatapp.models import Chat, Message
from config.utils.tests import data
from workroomsapp.models import City, Person, Domain, Lecture


class TestChatCreate(APITestCase):
    signup_data = data.SIGNUP.copy()
    signup_data2 = data.SIGNUP2.copy()
    profile_data = data.PROFILE.copy()
    lecturer_data = data.LECTURER.copy()
    customer_data = data.CUSTOMER.copy()
    lecture_data = data.LECTURE.copy()

    def setUp(self):
        temp_data = self.lecture_data.copy()
        self.client.post(reverse('signup'), self.signup_data)
        user = User.objects.get(email=self.signup_data['email'])
        Person.objects.create(
            user=user,
            **self.profile_data,
            city=City.objects.create(name='Москова')
        )
        Domain.objects.create(pk=1, name='Канцелярия')
        Domain.objects.create(pk=2, name='Бухгалтерия')
        Domain.objects.create(pk=3, name='Юриспруденция')

        self.client.post(reverse('lecturer'), self.lecturer_data)
        temp_data = self.lecture_data.copy()
        self.client.post(reverse('lecture_as_lecturer'), temp_data)

        self.client.post(reverse('signup'), self.signup_data2)
        user = User.objects.get(email=self.signup_data2['email'])
        Person.objects.create(
            user=user,
            **self.profile_data,
            city=City.objects.create(name='Москова')
        )
        self.client.post(reverse('customer'), self.customer_data)

    def test_chat_create(self):
        lecture = Lecture.objects.first()
        response = self.client.get(reverse('lecture_response'), {
            'lecture': lecture.pk,
            'date': (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%Y-%m-%dT%H:%M')
        })
        self.assertEqual(Chat.objects.all().exists(), True, msg='Чат не был создан \n'
                                                                f'Ответ: {response.data}')
        self.assertEqual(Message.objects.all().exists(), True, msg='Сообщение не было создано')

