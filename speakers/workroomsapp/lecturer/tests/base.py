from django.urls import reverse

from workroomsapp.models import Domain
from workroomsapp.person.tests.base import PersonCreateTestCase
from speakers.utils.tests import data


class BaseLecturerCreateTestCase(PersonCreateTestCase):
    """ Базовый класс для тестирования """

    lecturer_data = data.LECTURER.copy()

    def setUp(self):
        super().setUp()
        Domain.objects.get_or_create(pk=1, name='Канцелярия')
        Domain.objects.get_or_create(pk=2, name='Бухгалтерия')
        Domain.objects.get_or_create(pk=3, name='Юриспруденция')


class LecturerCreateTestCase(BaseLecturerCreateTestCase):
    """ Базовый класс для тестирования, в котором создается профиль лектора """

    def setUp(self):
        super().setUp()
        self.client.post(reverse('lecturer'), self.lecturer_data)
