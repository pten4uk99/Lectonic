from django.core import exceptions
from django.db import models, transaction

from workroomsapp import models as workrooms_models


class CustomerManager(models.Manager):
    @transaction.atomic
    def create_customer(self, person: object = None, domain: list = None,
                        hall_address: str = None, equipment: str = None):
        if not person:
            raise exceptions.ValidationError('Обязательное поле Person не заполнено')

        optional = workrooms_models.Optional.objects.create(
            hall_address=hall_address,
            equipment=equipment
        )

        customer = workrooms_models.Customer.objects.create(
            person=person, optional=optional)

        if domain is not None:
            for name in domain:
                workrooms_models.CustomerDomain.objects.create(
                    customer=customer,
                    domain=workrooms_models.Domain.objects.get(name=name)
                )

        calendar = workrooms_models.Calendar.objects.create()
        workrooms_models.CustomerCalendar.objects.create(
            customer=customer, calendar=calendar
        )

        person.is_customer = True
        person.save()

        return customer
