from django.core import exceptions
from django.db import models, transaction
from django.utils.timezone import make_aware

from workroomsapp import models as workrooms_models


class LectureManager(models.Manager):
    @transaction.atomic
    def __create_dependences(self, **kwargs):
        if not kwargs.get('lecturer'):
            raise exceptions.ValidationError(
                'В объектный менеджер не передан объект лектора')
        if not kwargs.get('lecture_type'):
            raise exceptions.ValidationError('В менеджер не передан тип лекции')

        optional = workrooms_models.Optional.objects.create(
            hall_address=kwargs.get('hall_address'),
            equipment=kwargs.get('equipment')
        )

        lecture = self.create(
            name=kwargs.get('name'),
            svg=kwargs.get('svg'),
            optional=optional,
            type=kwargs.get('lecture_type'),
            listeners=kwargs.get('listeners'),
            cost=kwargs.get('cost'),
            description=kwargs.get('description')
        )

        if kwargs.get('domain') is not None:
            for name in kwargs.get('domain'):
                workrooms_models.LectureDomain.objects.create(
                    lecture=lecture,
                    domain=workrooms_models.Domain.objects.get(name=name)
                )

        if kwargs.get('lecturer'):
            lecture.lecturer = kwargs['lecturer']
            calendar = kwargs['lecturer'].lecturer_calendar.calendar
        elif kwargs.get('customer'):
            lecture.customer = kwargs['customer']
            calendar = kwargs['customer'].customer_calendar.calendar

        for event in kwargs.get('datetime'):
            lecture_request = workrooms_models.LectureRequest.objects.create(lecture=lecture)
            calendar.events.add(workrooms_models.Event.objects.create(
                datetime_start=make_aware(event[0]),
                datetime_end=make_aware(event[1]),
                lecture_request=lecture_request))

        lecture.save()
        calendar.save()
        return lecture

    def create_as_lecturer(self, **kwargs):
        return self.__create_dependences(**kwargs)

    def create_as_customer(self, **kwargs):
        return self.__create_dependences(**kwargs)
