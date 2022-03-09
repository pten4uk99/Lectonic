import datetime

from django.urls import reverse
from rest_framework.test import APITestCase

from authapp.models import User
from workroomsapp.models import City, Person, Domain, Lecturer, Customer


class TestLectureCreate(APITestCase):
    signup_data = {'email': 'admin@admin.ru', 'password': '12345678'}
    profile_data = {
        'first_name': 'Пётр-Петр',
        'last_name': 'Петр',
        'middle_name': 'Петрович',
        'birth_date': '2020-01-18',
        'description': 'Описанюшка',
    }
    lecturer_data = {
        'domain': ['1', '2', '3'],
        'performances_links': [
            'https://dev.lectonic.ru/city/?name=Москова',
            'http://dev.lectonic.com/com/com'
        ],
        'publication_links': [
            'https://dev.lectonic.ru/city/?name=Москова',
            'http://dev.lectonic.com/com/com'
        ],
        'education': 'У меня нереально высокое образование, я прям не могу',
        'hall_address': 'Москва, ул. Не московская, д. Домашний',
        'equipment': 'Руки, ноги, доска, полет.'
    }
    lecture_data = {
        'name': 'Лекция супер хорошая лекция',
        'datetime': datetime.datetime.now() - datetime.timedelta(days=5),
        'hall_address': 'Москва, ул. Не московская, д. Домашний',
        'type': 'offline',
        'equipment': 'Руки, ноги, доска, полет.',
        'duration': '30',
        'cost': '1000',
        'description': 'Отличное описание блин'
    }

    def setUp(self):
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

    # def test_lecture_as_lecturer_was_created(self):
    #     response = self.client.post(reverse('lecture'), self.lecture_data)
    #     print(response.data)
    #     # self.assertEqual(
    #     #     response.status_code, 201,
    #     #     msg='Неверный статус ответа при создании профиля заказчика'
    #     # )
