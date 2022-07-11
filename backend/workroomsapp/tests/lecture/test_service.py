from rest_framework.test import APITestCase

from services.api import service_delete_lecture_by_id
from workroomsapp.models import Lecturer, Lecture
from workroomsapp.tests.managers import LecturerTestManager, CustomerTestManager, LectureTestManager


class LectureServiceTestCase(APITestCase):
    def setUp(self):
        l_manager = LecturerTestManager()
        c_manager = CustomerTestManager()
        l_manager.create_obj()
        c_manager.create_obj()

        lecture_manager = LectureTestManager(Lecturer.objects.first())
        lecture_manager.create_obj(3)

    def test_delete_lecture_by_id(self):
        lecture_count = Lecture.objects.all().count()
        service_delete_lecture_by_id(Lecturer.objects.first().person.user, Lecture.objects.first().pk)

        self.assertEqual(
            lecture_count - 1,
            Lecture.objects.all().count(),
            msg="Неверное количество лекций после удаления лекции"
        )
