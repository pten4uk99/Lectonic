from django.urls import reverse

from authapp.models import User
from workroomsapp.customer.tests.base import BaseCustomerCreateTestCase

from workroomsapp.models import Person, Customer


class TestCustomerCreate(BaseCustomerCreateTestCase):
    def setUp(self):
        super().setUp()

    def test_customer_was_created(self):
        temp_data = self.customer_data.copy()
        response = self.client.post(reverse('customer'), temp_data)
        self.assertEqual(
            response.status_code, 201,
            msg='Неверный статус ответа при создании профиля заказчика\n'
                f'Ошибка: {response.data}'
        )
        self.assertEqual(
            Customer.objects.filter(person=Person.objects.get(user=User.objects.first())).exists(),
            True,
            msg='Заказчик не был создан в базе данных'
        )

    def test_credentials(self):
        temp_data = self.customer_data.copy()
        self.client.get(reverse('logout'))

        response = self.client.post(reverse('customer'), temp_data)
        self.assertEqual(
            response.status_code, 401,
            msg='Неверный статус ответа при попытке создания профиля заказчика неавторизованным пользователем'
        )

    def test_wrong_domain(self):
        temp_data = self.customer_data.copy()
        temp_data['domain'] = ['privet']

        response = self.client.post(reverse('customer'), temp_data)
        self.assertEqual(
            response.status_code, 400,
            msg='Неверный статус ответа при неверно переданной тематике лекции'
        )
