import datetime

from django.urls import reverse
from rest_framework.test import APITestCase, override_settings

from speakers.utils.tests import data
from speakers.utils.tests.upload_image import test_image
from workroomsapp.models import City, Domain


@override_settings(MEDIA_URL=test_image.MEDIA_URL, MEDIA_ROOT=test_image.MEDIA_ROOT)
class TestLecturerCalendarGet(APITestCase):
    signup_data = data.SIGNUP.copy()
    profile_data = data.PROFILE.copy()
    profile_data['city'] = '1'
    lecturer_data = data.LECTURER.copy()

    def setUp(self):
        temp_signup_data = self.signup_data.copy()
        temp_profile_data = self.profile_data.copy()
        temp_profile_data['photo'] = test_image.create_image()
        temp_lecturer_data = self.lecturer_data.copy()

        City.objects.create(pk=1, name='Москова')
        Domain.objects.create(pk=1, name='Москова')
        Domain.objects.create(pk=2, name='Инопришленец')
        Domain.objects.create(pk=3, name='Колхоз')

        self.client.post(reverse('signup'), temp_signup_data)
        self.client.post(reverse('profile'), temp_profile_data)
        self.client.post(reverse('lecturer'), temp_lecturer_data)

        self.client.post(reverse('lecture_as_lecturer'),
                         {
                             'name': 'Моя лектушка',
                             'photo': test_image.create_image(),
                             'domain': ['1', '2', '3'],
                             'datetime': '2022-03-12',
                             'duration': '30',
                             'type': 'offline'
                         })
        self.client.post(reverse('lecture_as_lecturer'),
                         {
                             'name': 'Твоя лектушка',
                             'photo': test_image.create_image(),
                             'domain': ['1', '2', '3'],
                             'datetime': '2022-03-12',
                             'duration': '30',
                             'type': 'offline'
                         })
        self.client.post(reverse('lecture_as_lecturer'),
                         {
                             'name': 'Ее лектушка',
                             'photo': test_image.create_image(),
                             'domain': ['1', '2', '3'],
                             'datetime': '2022-03-12',
                             'duration': '30',
                             'type': 'offline'
                         })
        self.client.post(reverse('lecture_as_lecturer'),
                         {
                             'name': 'Его лектушка',
                             'photo': test_image.create_image(),
                             'domain': ['1', '2', '3'],
                             'datetime': '2022-03-18',
                             'duration': '30',
                             'type': 'offline'
                         })

    def test_get_calendar(self):
        response = self.client.get(
            reverse('lecturer_calendar'), {'year': 2022, 'month': 3})
        self.assertEqual(
            'data' in response.data and type(response.data['data']) == list, True,
            msg='В ответе нет списка data'
        )
        self.assertEqual(
            'date' in response.data['data'][0], True,
            msg='В словаре списка data нет ключа date'
        )
        self.assertEqual(
            len(response.data['data'][0]['events']), 3,
            msg='Неверное количество событий'
        )
