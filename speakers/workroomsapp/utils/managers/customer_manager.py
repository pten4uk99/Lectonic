from django.core import exceptions
from django.db import models, transaction

from workroomsapp import models as workrooms_models


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
