from rest_framework.test import APITestCase

from services.filters.base import FilterBackend
from services.filters.lecture import WithoutPermanentLectureFilter, FutureLectureFilter, CreatedLecturerLectureFilter, \
    PermanentLectureFilter
from workroomsapp.models import Lecturer, Lecture, Customer, City, Domain, LectureDomain
from workroomsapp.tests.managers import LecturerTestManager, CustomerTestManager, LectureTestManager


class FilterTestCase(APITestCase):
    def setUp(self):
        self.l_manager = LecturerTestManager()
        self.c_manager = CustomerTestManager()
        self.l_manager.create_obj()
        self.c_manager.create_obj()
        
        self.l_lecture_manager = LectureTestManager(Lecturer.objects.first())
        self.c_lecture_manager = LectureTestManager(Customer.objects.first())
        self.l_lecture_manager.create_obj(2)
        self.c_lecture_manager.create_obj(1)
        
        self.new_city = City.objects.create(pk=2, name='Устькузьминск')
        self.new_domain = Domain.objects.create(pk=4, name='Индустрия')
        
        self.user = Lecturer.objects.first().person.user
        lecture_domain = LectureDomain.objects.create(
            lecture=self.l_lecture_manager.obj, domain=self.new_domain)
        self.l_lecture_manager.obj.lecture_domains.set([lecture_domain])
        self.l_lecture_manager._creator.person.city = self.new_city
        self.l_lecture_manager._creator.person.save()
        self.l_lecture_manager.create_obj()
        del self.l_lecture_manager.data['datetime']
        self.l_lecture_manager.create_obj()
        
        lecture = Lecture.objects.first()
        lecture_request = lecture.lecture_requests.first()
        lecture_request.respondents.add(Customer.objects.first().person)
        lecture_request.save()
        respondent = lecture_request.respondent_obj.first()
        respondent.confirmed = True
        respondent.save()
    
    def test_setup(self):
        lectures = Lecture.objects.all()
        assert lectures.filter(lecture_requests=None).exists()
        assert lectures.filter(lecture_requests__respondent_obj__confirmed=True).exists()
    
    def test_created_lectures_filter(self):
        filter_backend = FilterBackend(
            from_obj=self.user,
            qs=Lecture.objects.all(),
            filter_classes=[CreatedLecturerLectureFilter,
                            WithoutPermanentLectureFilter,
                            FutureLectureFilter],
            filter_query={'city': self.new_city.pk, 'domain': self.new_domain.pk}
        )
        
        filtered = filter_backend.filter_queryset()
        
        for lecture in filtered:
            lecture: Lecture
            assert lecture.lecturer
            assert lecture.lecturer.person.city == self.new_city, 'Неверно отфильтрован город'
            assert lecture.lecture_domains.filter(domain=self.new_domain), 'Не верно отфильтрованы тематики'
            assert lecture.lecture_requests.all().exists(), 'Не верно отфильтрованы лекции'

    def test_permanent_lecture_filter(self):
        filter_backend = FilterBackend(
            from_obj=self.user,
            qs=Lecture.objects.all(),
            filter_classes=[PermanentLectureFilter],
        )
    
        filtered = filter_backend.filter_queryset()
        
        for lecture in filtered:
            lecture: Lecture
            assert not lecture.lecture_requests.all().exists(), 'Не верно отфильтрованы лекции'
            assert lecture.lecturer.person.user == self.user, 'Не верно отфильтрованы лекции'
    