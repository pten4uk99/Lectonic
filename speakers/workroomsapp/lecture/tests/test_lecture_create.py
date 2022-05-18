from workroomsapp.lecture.tests.base import (
    BaseLectureAsLecturerCreateTestCase,
    BaseLectureAsCustomerCreateTestCase
)


class TestLectureAsLecturerCreate(BaseLectureAsLecturerCreateTestCase):
    def setUp(self):
        super().setUp()

    def test_lecture_was_created(self):
        self.make_create_tests()

    def test_with_existing_datetime(self):
        self.make_test_existing_datetime()


class TestLectureAsCustomerCreate(BaseLectureAsCustomerCreateTestCase):
    def setUp(self):
        super().setUp()

    def test_lecture_was_created(self):
        self.make_create_tests()

    def test_with_existing_datetime(self):
        self.make_test_existing_datetime()
