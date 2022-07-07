from django.urls import reverse

from workroomsapp.lecturer.tests.base import BaseLecturerCreateTestCase
from config.utils.tests import data


class BaseCustomerCreateTestCase(BaseLecturerCreateTestCase):
    """ Базовый класс для тестирования """
    signup_data = data.SIGNUP2.copy()
    customer_data = data.CUSTOMER.copy()

    def setUp(self):
        super().setUp()


class CustomerCreateTestCase(BaseCustomerCreateTestCase):
    """ Базовый класс для тестирования, в котором создается профиль заказчика """

    def setUp(self):
        super().setUp()
        self.client.post(reverse('customer'), self.customer_data)
