from workroomsapp.models import Lecture
from workroomsapp.tests.base import BaseLectureAsLecturerCreateTestCase, BaseLectureAsCustomerCreateTestCase


class TestLectureAsLecturerCreate(BaseLectureAsLecturerCreateTestCase):
    def setUp(self):
        super().setUp()

    def test_lecture_was_created(self):
        self.make_create_tests()
        
    def test_permanent_lecture_create(self):
        temp_data = self.lecture_data.copy()
        del temp_data['datetime']
        response = self.make_request(temp_data)
        self.assertEqual(Lecture.objects.filter(lecture_requests=None).exists(), True)

    def test_with_existing_datetime(self):
        self.make_test_existing_datetime()


class TestLectureAsCustomerCreate(BaseLectureAsCustomerCreateTestCase):
    def setUp(self):
        super().setUp()

    def test_lecture_was_created(self):
        self.make_create_tests()

    def test_with_existing_datetime(self):
        self.make_test_existing_datetime()
