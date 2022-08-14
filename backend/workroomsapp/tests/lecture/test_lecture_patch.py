from datetime import datetime, timedelta

from django.urls import reverse

from workroomsapp.models import Lecturer, Lecture, Domain
from workroomsapp.tests.base import BaseLectureAsLecturerCreateTestCase


class LecturePatchTestCase(BaseLectureAsLecturerCreateTestCase):
    def setUp(self):
        super().setUp()
        self.client.post(reverse('lecture_as_lecturer_create_list'), self.lecture_data)

    def test_lecture_patch(self):
        new_domains = ['Эквилибристика', 'Лалалэнд']
        new_datetime_start = datetime.now() + timedelta(days=5)
        new_datetime_end = datetime.now() + timedelta(days=5, hours=1)

        for index, name in enumerate(new_domains):
            Domain.objects.create(name=name, pk=index + 4)

        temp_data = {
            'name': 'Обновленное название лекции',
            'domain': new_domains,
            'datetime': [
                (new_datetime_start.strftime('%Y-%m-%dT%H:%M')) +
                ',' +
                (new_datetime_end.strftime('%Y-%m-%dT%H:%M'))],
            'type': 'Офлайн',
            'cost': 7200,
            'description': 'Обновленное описание лекции',
            'hall_address': 'Обновленный адрес',
            'equipment': 'Обновленное оборудование'
        }

        self.client.patch(reverse('lecture_as_lecturer_update_delete', args=[Lecture.objects.first().pk]), temp_data)
        lecture = Lecture.objects.first()

        self.assertEqual(lecture.name, temp_data['name'], msg='Название лекции не изменилось')
        self.assertEqual(
            list(lecture.lecture_domains.all().values_list('domain__name', flat=True)), temp_data['domain'],
            msg='Тематики лекции не изменились'
        )
        self.assertEqual(
            lecture.lecture_requests.first().event.datetime_start.day, new_datetime_start.day,
            msg='Даты лекции не изменились'
        )
