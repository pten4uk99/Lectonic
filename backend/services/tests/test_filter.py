from rest_framework.test import APITestCase

from services.filters import CreatedLecturerLectureFilter
from services.filters.lecture import PotentialCustomerLectureFilter
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
        
        lecture = Lecture.objects.first()
        lecture_request = lecture.lecture_requests.first()
        lecture_request.respondents.add(Customer.objects.first().person)
        lecture_request.save()
        respondent = lecture_request.respondent_obj.first()
        respondent.confirmed = True
        respondent.save()
    
    def test_get_created_lectures(self):
        new_city = City.objects.create(pk=2, name='Устькузьминск')
        new_domain = Domain.objects.create(pk=4, name='Индустрия')
        
        user = Lecturer.objects.first().person.user
        lecture_domain = LectureDomain.objects.create(
            lecture=self.l_lecture_manager.obj, domain=new_domain)
        self.l_lecture_manager.obj.lecture_domains.set([lecture_domain])
        self.l_lecture_manager._creator.person.city = new_city
        self.l_lecture_manager._creator.person.save()
        self.l_lecture_manager.create_obj()
        filter_class = CreatedLecturerLectureFilter(from_obj=user, city=new_city.pk, domain=new_domain.pk)
        
        self.assertEqual(
            filter_class.filter().values('lecturer__person__city__name')[0].get('lecturer__person__city__name'),
            new_city.name,
            msg='Неверно отфильтрованы лекции'
        )
        
        self.assertEqual(
            filter_class.filter().values('lecture_domains__domain__name')[0].get('lecture_domains__domain__name'),
            new_domain.name,
            msg='Неверно отфильтрованы лекции'
        )
    
    # def test_get_potential_lectures(self):
    #     new_city = City.objects.create(pk=2, name='Карачаево')
    #     new_domain = Domain.objects.create(pk=4, name='Молоко')
    #
    #     user = Lecturer.objects.last().person.user
    #     lecture_domain = LectureDomain.objects.create(
    #         lecture=self.l_lecture_manager.obj, domain=new_domain)
    #     self.l_lecture_manager.obj.lecture_domains.set([lecture_domain])
    #     self.l_lecture_manager._creator.person.city = new_city
    #     self.l_lecture_manager._creator.person.save()
    #     self.l_lecture_manager.create_obj()
    #
    #     filter_class = PotentialCustomerLectureFilter(from_obj=user, city=new_city.pk, domain=new_domain.pk)
    #     # print(filter_class.filter())
    #     self.assertEqual(
    #         filter_class.filter().values('lecturer__person__city__name')[0].get('lecturer__person__city__name'),
    #         new_city.name,
    #         msg='Неверно отфильтрованы лекции'
    #     )
    #
    #     self.assertEqual(
    #         filter_class.filter().values('lecture_domains__domain__name')[0].get('lecture_domains__domain__name'),
    #         new_domain.name,
    #         msg='Неверно отфильтрованы лекции'
    #     )
    #
    # def test_get_confirmed_lectures(self):
    #     new_city_name = 'Карачаево'
    #     new_domain = 'Молоко'
    #
    #     user = Lecturer.objects.first().person.user
    #     lecture_domain = LectureDomain.objects.create(
    #         lecture=self.l_lecture_manager.obj, domain=Domain.objects.create(pk=4, name=new_domain))
    #     self.c_lecture_manager.obj.lecture_domains.set([lecture_domain])
    #     self.c_lecture_manager._creator.person.city = City.objects.create(name=new_city_name, pk=2)
    #     self.c_lecture_manager._creator.person.save()
    #     self.c_lecture_manager.create_obj()
    #
    #     filter_class = PotentialCustomerLectureFilter(from_obj=user, city=new_city_name, domain=new_domain)
    #
    #     self.assertEqual(
    #         filter_class.filter().values('customer__person__city__name')[0].get('customer__person__city__name'),
    #         new_city_name,
    #         msg='Неверно отфильтрованы лекции'
    #     )
    #
    #     self.assertEqual(
    #         filter_class.filter().values('lecture_domains__domain__name')[0].get('lecture_domains__domain__name'),
    #         new_domain,
    #         msg='Неверно отфильтрованы лекции'
    #     )
