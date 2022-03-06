from django.urls import reverse
from rest_framework.test import APITestCase

from authapp.models import User
from workroomsapp.models import City, Person, Domain, Lecturer


class TestLecturerCreate(APITestCase):
    data = {
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

    def setUp(self):
        signup_data = {'email': 'admin@admin.ru', 'password': '12345678'}
        self.client.post(reverse('signup'), signup_data)
        profile_data = {
            'first_name': 'Пётр-Петр',
            'last_name': 'Петр',
            'middle_name': 'Петрович',
            'birth_date': '2020-01-18',
            'city': City.objects.create(name='Москова'),
            'description': 'Описанюшка',
        }
        user = User.objects.get(email=signup_data['email'])
        Person.objects.create(
            user=user,
            **profile_data
        )
        Domain.objects.create(pk=1, name='Канцелярия')
        Domain.objects.create(pk=2, name='Бухгалтерия')
        Domain.objects.create(pk=3, name='Юриспруденция')

    def test_lecturer_was_created(self):
        response = self.client.post(reverse('lecturer'), self.data)
        self.assertEqual(
            response.status_code, 201,
            msg='Неверный статус ответа при создании профиля лектора'
        )
        self.assertEqual(
            Lecturer.objects.filter(person=Person.objects.get(user=User.objects.first())).exists(),
            True,
            msg='Лектор не был создан в базе данных'
        )

    def test_credentials(self):
        self.client.get(reverse('logout'))

        response = self.client.post(reverse('lecturer'), self.data)
        self.assertEqual(
            response.status_code, 401,
            msg='Неверный статус ответа при попытке создания профиля лектора неавторизованным пользователем'
        )

    def test_wrong_domain(self):
        self.data['domain'] = ['privet']

        response = self.client.post(reverse('lecturer'), self.data)
        self.assertEqual(
            response.status_code, 400,
            msg='Неверный статус ответа при неверно переданной тематике лекции'
        )
