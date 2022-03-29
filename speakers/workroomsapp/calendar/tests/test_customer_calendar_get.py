import datetime

from django.urls import reverse
from rest_framework.test import APITestCase, override_settings

from speakers.utils.tests import data
from speakers.utils.tests.upload_image import test_image
from workroomsapp.models import City, Domain


@override_settings(MEDIA_URL=test_image.MEDIA_URL, MEDIA_ROOT=test_image.MEDIA_ROOT)
class TestCustomerCalendarGet(APITestCase):
    signup_data = data.SIGNUP.copy()
    profile_data = data.PROFILE.copy()
    profile_data['city'] = '1'
    customer_data = data.CUSTOMER.copy()

    def setUp(self):
        temp_signup_data = self.signup_data.copy()
        temp_profile_data = self.profile_data.copy()
        temp_profile_data['photo'] = test_image.create_image()
        temp_customer_data = self.customer_data.copy()

        City.objects.create(pk=1, name='Москова')
        Domain.objects.create(pk=1, name='Канцелярия')
        Domain.objects.create(pk=2, name='Бухгалтерия')
        Domain.objects.create(pk=3, name='Юриспруденция')

        self.client.post(reverse('signup'), temp_signup_data)
        self.client.post(reverse('profile'), temp_profile_data)
        self.client.post(reverse('customer'), temp_customer_data)

        for i in range(3):
            self.client.post(reverse('lecture_as_customer'),
                             {
                                 'name': f'Моя лектушка {i}',
                                 'photo': test_image.create_image(),
                                 'domain': ['Канцелярия', 'Бухгалтерия', 'Юриспруденция'],
                                 'datetime': [str(datetime.datetime.now() + datetime.timedelta(days=2 + i)) + ',' +
                                              str(datetime.datetime.now() + datetime.timedelta(days=2 + i, hours=1))],
                                 'listeners': '30',
                                 'type': 'offline'
                             })
        for i in range(4, 7):
            self.client.post(reverse('lecture_as_customer'),
                             {
                                 'name': f'Моя лектушка {i}',
                                 'photo': test_image.create_image(),
                                 'domain': ['Канцелярия', 'Бухгалтерия', 'Юриспруденция'],
                                 'datetime': [str(datetime.datetime.now() + datetime.timedelta(days=2 + i)) + ',' +
                                              str(datetime.datetime.now() + datetime.timedelta(days=2 + i, hours=1))],
                                 'listeners': '30',
                                 'type': 'offline'
                             })

    def test_get_calendar(self):
        response = self.client.get(
            reverse('customer_calendar'), {'year': datetime.datetime.now().year,
                                           'month': datetime.datetime.now().month})
        # Если уже конец месяца, то события могут отображаться некорректно
        self.assertEqual(
            'data' in response.data and type(response.data['data']) == list, True,
            msg='В ответе нет списка data'
        )
        self.assertEqual(
            'date' in response.data['data'][0], True,
            msg='В словаре списка data нет ключа date'
        )
        self.assertEqual(
            len(response.data['data'][0]['events']), 1,
            msg='Неверное количество событий'
        )
        self.assertEqual(
            len(response.data['data'][1]['events']), 1,
            msg='Неверное количество событий'
        )
        self.assertEqual(
            len(response.data['data'][2]['events']), 2,
            msg='Неверное количество событий'
        )