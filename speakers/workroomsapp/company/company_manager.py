from django.core import exceptions
from django.db import models, transaction

from workroomsapp import models as workrooms_models


class CompanyManager(models.Manager):
    @transaction.atomic
    def create_company(self, person: object = None,
                       name: str = None, company_form: int = None,
                       specialization: str = None, document: object = None,
                       representative_person: dict = None, legal_address: str = None,
                       actual_address: str = None, optional: object = None,
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
            actual_address=actual_address,
            is_verified=is_verified,
            optional=optional
        )
        workrooms_models.CompanyCalendar.objects.create(company=company, calendar=calendar)

        return company
