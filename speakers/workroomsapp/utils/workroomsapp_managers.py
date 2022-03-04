from django.core import exceptions
from django.db import models, transaction

from workroomsapp import models as workrooms_models


class LectureManager(models.Manager):
    @transaction.atomic
    def __create_dependences(self, name: str, datetime: object = None,
                             optional: dict = None, status: bool = None,
                             duration: int = None, cost: int = 0, description: str = ""):
        new_optional = None

        if optional is not None:
            new_optional = workrooms_models.Optional.objects.create(
                hall_address=optional.get('hall_address'),
                equipment=optional.get('equipment')
            )

        lecture = self.create(
            name=name,
            optional=new_optional or None,
            status=status or None,
            duration=duration or None,
            cost=cost,
            description=description or None
        )

        event = workrooms_models.Event.objects.create(datetime=datetime)

        return workrooms_models.LectureRequest.objects.create(lecture=lecture, event=event)

    @transaction.atomic
    def create_as_lecturer(self, name: str, lecturer: object = None,
                           datetime: object = None, optional: dict = None,
                           status: bool = None, duration: int = None, cost: int = 0,
                           description: str = ""):
        lecture_request = self.__create_dependences(
            name=name,
            datetime=datetime,
            optional=optional,
            status=status,
            duration=duration,
            cost=cost,
            description=description
        )

        if not lecturer:
            raise exceptions.ValidationError(
                'В объектный менеджер не передан объект лектора')

        if lecturer.lecturer_calendar:
            calendar = lecturer.lecturer_calendar.calendar
            calendar.events.add(lecture_request.event)
            calendar.save()

        return workrooms_models.LecturerLectureRequest.objects.create(
            lecturer=lecturer,
            lecture_request=lecture_request
        )


class LecturerManager(models.Manager):
    @transaction.atomic
    def create_lecturer(self, person: object = None, performances_links: list = None,
                        publication_links: list = None, domain: list = None,
                        diploma_image: list = None, hall_address: str = None,
                        equipment: str = None, education: str = None):
        if not person:
            raise exceptions.ValidationError('Обязательное поле Person не заполнено')

        optional = workrooms_models.Optional.objects.create(
            hall_address=hall_address,
            equipment=equipment
        )

        lecturer = workrooms_models.Lecturer.objects.create(
            person=person,
            optional=optional,
            education=education
        )

        if domain is not None:
            for domain_id in domain:
                workrooms_models.LecturerDomain.objects.create(lecturer=lecturer, domain=domain_id)
        if performances_links is not None:
            for perf_link in performances_links:
                lecturer.performances_links.add(workrooms_models.Link.objects.create(perf_link))
        if publication_links is not None:
            for pub_link in publication_links:
                lecturer.publication_links.add(pub_link)

        for image in diploma_image:
            workrooms_models.DiplomaImage.objects.create(
                lecturer=lecturer,
                image=workrooms_models.Image.objects.create(photo=image))

        calendar = workrooms_models.Calendar.objects.create()
        workrooms_models.LecturerCalendar.objects.create(
            lecturer=lecturer, calendar=calendar)

        person.is_lecturer = True
        person.save()

        return lecturer


class CustomerManager(models.Manager):
    @transaction.atomic
    def create_customer(self, person: object = None, optional: object = None):
        if not person:
            raise exceptions.ValidationError('Обязательное поле Person не заполнено')

        calendar = workrooms_models.Calendar.objects.create()
        customer = workrooms_models.Customer.objects.create(
            person=person, optional=optional)
        workrooms_models.CustomerCalendar.objects.create(
            customer=customer, calendar=calendar)

        return customer


class CompanyManager(models.Manager):
    @transaction.atomic
    def create_company(self, person: object = None,
                       name: str = None, company_form: (int, object) = None,
                       specialization: str = None, document: object = None,
                       representative_person: dict = None, legal_address: str = None,
                       actial_address: str = None, optional: object = None,
                       is_verified: bool = False):
        if not person:
            raise exceptions.ValidationError('Обязательное поле person не заполнено')
        if not document:
            raise exceptions.ValidationError('Обязательное поле document не заполнено')
        if not name:
            raise exceptions.ValidationError('Обязательное поле name не заполнено')

        calendar = workrooms_models.Calendar.objects.create()
        representative_person = workrooms_models.RepresentativePerson.objects.create(
            first_name=representative_person.get('first_name', person.first_name),
            last_name=representative_person.get('last_name', person.last_name),
            middle_name=representative_person.get('middle_name', person.middle_name),
        )
        company = workrooms_models.Company.objects.create(
            person=person,
            name=name,
            company_form=company_form,
            specialization=specialization,
            document=document,
            representative_person=representative_person,
            legal_address=legal_address,
            actial_address=actial_address,
            is_verified=is_verified,
            optional=optional
        )
        workrooms_models.CompanyCalendar.objects.create(company=company, calendar=calendar)

        return company
