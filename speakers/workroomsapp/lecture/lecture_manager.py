from django.core import exceptions
from django.db import models, transaction
from django.utils.timezone import make_aware

from workroomsapp import models as workrooms_models


class LectureManager(models.Manager):
    @transaction.atomic
    def create_as_lecturer(self, name: str, cost: int = 0, svg: int = None,
                           lecturer: object = None, datetime: list = None,
                           hall_address: str = None, equipment: str = None,
                           lecture_type: str = None,
                           description: str = "", domain: list = None):

        if not lecturer:
            raise exceptions.ValidationError(
                'В объектный менеджер не передан объект лектора')
        if not lecture_type:
            raise exceptions.ValidationError('В менеджер не передан тип лекции')

        optional = workrooms_models.Optional.objects.create(
            hall_address=hall_address,
            equipment=equipment
        )

        lecture = self.create(
            name=name,
            svg=svg,
            optional=optional,
            type=lecture_type,
            lecturer=lecturer,
            cost=cost,
            description=description
        )

        if domain is not None:
            for name in domain:
                workrooms_models.LectureDomain.objects.create(
                    lecture=lecture,
                    domain=workrooms_models.Domain.objects.get(name=name)
                )

        calendar = lecturer.lecturer_calendar.calendar
        for event in datetime:
            lecture_request = workrooms_models.LectureRequest.objects.create(lecture=lecture)
            calendar.events.add(workrooms_models.Event.objects.create(
                datetime_start=make_aware(event[0]),
                datetime_end=make_aware(event[1]),
                lecture_request=lecture_request))

        calendar.save()

        return lecture

    @transaction.atomic
    def create_as_customer(self, name: str, svg: int = None,
                           customer: object = None, datetime: list = None,
                           hall_address: str = None, equipment: str = None,
                           lecture_type: str = None,
                           listeners: int = None, cost: int = 0,
                           description: str = "", domain: list = None):

        if not customer:
            raise exceptions.ValidationError(
                'В объектный менеджер не передан объект лектора')
        if not lecture_type:
            raise exceptions.ValidationError('В менеджер не передан тип лекции')

        optional = workrooms_models.Optional.objects.create(
            hall_address=hall_address,
            equipment=equipment
        )

        lecture = self.create(
            name=name,
            svg=svg,
            optional=optional,
            type=lecture_type,
            customer=customer,
            listeners=listeners,
            cost=cost,
            description=description
        )

        if domain is not None:
            for name in domain:
                workrooms_models.LectureDomain.objects.create(
                    lecture=lecture,
                    domain=workrooms_models.Domain.objects.get(name=name)
                )

        calendar = customer.customer_calendar.calendar
        for event in datetime:
            lecture_request = workrooms_models.LectureRequest.objects.create(lecture=lecture)
            calendar.events.add(workrooms_models.Event.objects.create(
                datetime_start=make_aware(event[0]),
                datetime_end=make_aware(event[1]),
                lecture_request=lecture_request))

        calendar.save()

        return lecture
