from django.urls import reverse

from authapp.models import User
from workroomsapp.tests.base import BaseLecturerCreateTestCase
from workroomsapp.models import Person, Lecturer


class TestLecturer(BaseLecturerCreateTestCase):
    def setUp(self):
        super().setUp()

    def test_lecturer_was_created(self):
        temp_data = self.lecturer_data.copy()
        response = self.client.post(reverse('lecturer'), temp_data)
        self.assertEqual(
            response.status_code, 201,
            msg='Неверный статус ответа при создании профиля лектора'
        )
        self.assertEqual(
            Lecturer.objects.filter(person=Person.objects.get(user=User.objects.first())).exists(),
            True,
            msg='Лектор не был создан в базе данных'
        )

    def test_lecturer_success_get(self):
        self.client.post(reverse('lecturer'), self.lecturer_data)
        response = self.client.get(reverse('lecturer'), {'id': Lecturer.objects.first().pk})
        self.assertEqual(
            response.status_code, 200,
            msg='Неверный статус ответа при получении профиля лектора\n'
                f'Ответ: {response.data}'
        )

    def test_credentials(self):
        temp_data = self.lecturer_data.copy()
        self.client.get(reverse('logout'))

        response = self.client.post(reverse('lecturer'), temp_data)
        self.assertEqual(
            response.status_code, 401,
            msg='Неверный статус ответа при попытке создания профиля лектора неавторизованным пользователем'
        )

    def test_wrong_domain(self):
        temp_data = self.lecturer_data.copy()
        temp_data['domain'] = ['privet']

        response = self.client.post(reverse('lecturer'), temp_data)
        self.assertEqual(
            response.status_code, 400,
            msg='Неверный статус ответа при неверно переданной тематике лекции'
        )
