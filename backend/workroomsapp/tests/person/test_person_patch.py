from django.urls import reverse

from workroomsapp.models import City
from workroomsapp.tests.base import PersonCreateTestCase


class TestPersonPatch(PersonCreateTestCase):
    def setUp(self):
        super().setUp()
        City.objects.create(name='Ярославль', pk=2)

    def test_credentials(self):
        self.client.get(reverse('logout'))
        response = self.client.patch(reverse('profile'), {'city': '2'})
        self.assertEqual(
            response.status_code, 401,
            msg='Неверный статус ответа при попытке изменения профиля неавторизованного пользователя'
        )

    def test_person_successful_patched(self):
        temp_data = {
            'first_name': 'Василий',
            'last_name': 'Головнов',
            'middle_name': 'Головиныч',
            'birth_date': '2018-01-18',
            'city': '2',
            'description': 'Новая описанюшка',
        }

        for key, value in temp_data.items():
            response = self.client.patch(reverse('profile'), {key: value})
            self.assertEqual(
                response.status_code, 200,
                msg=f'Неверный статус ответа при изменении поля {key} профиля пользователя'
            )

            if key == 'city':
                self.assertEqual(
                    response.data['data'][0]['city']['name'], 'Ярославль',
                    msg='Неверные данные в ответе при изменении города профиля пользователя'
                )

    def test_no_passed_data(self):
        response = self.client.patch(reverse('profile'))
        self.assertEqual(
            response.status_code, 400,
            msg=f'Не передано данных для изменения профиля пользователя'
        )

    def test_wrong_data(self):
        temp_data = {
            'first_name': 'Василий1',
            'last_name': 'ГоловновD',
            'middle_name': 1,
            'birth_date': '201801-18',
            'city': 'Ярославль',
        }

        for key, value in temp_data.items():
            response = self.client.patch(reverse('profile'), {key: value})
            self.assertEqual(
                response.status_code, 400,
                msg=f'Неверный статус ответа при неправильном изменении поля {key} профиля пользователя'
            )

        response = self.client.patch(reverse('profile'), {'city': '3'})
        self.assertEqual(
            response.status_code, 400,
            msg=f'Неверный статус ответа при неправильном изменении города профиля пользователя'
        )
