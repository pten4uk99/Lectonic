from django.core import exceptions
from django.db import models, transaction

from workroomsapp import models as workrooms_models


class LectureCreator:
    fields = [
        'lecturer',
        'customer',
        'name',
        'svg',
        'domain',
        'listeners',
        'datetime',
        'hall_address',
        'equipment',
        'type',
        'cost',
        'description',
    ]

    required_fields = [
        'svg',
        'type',
        'datetime',
    ]

    def __init__(self, **kwargs):
        for field in self.fields:
            setattr(self, field, kwargs.get(field, None))

        self.check_required_fields()

        self._is_lecturer = 'lecturer' in kwargs
        self.optional = None
        self.lecture = None
        self.calendar = self._get_calendar()

    def _get_calendar(self):
        if self._is_lecturer:
            return self.lecturer.lecturer_calendar.calendar
        return self.customer.customer_calendar.calendar

    def check_required_fields(self):
        for field in self.required_fields:
            if not hasattr(self, field):
                raise exceptions.ValidationError(f'Обязательный аргумент {field}')

        if not self.lecturer and not self.customer:
            raise exceptions.ValidationError('Обязателен один из аргументов (lecturer/customer)')

    def create_optional(self):
        self.optional = workrooms_models.Optional.objects.create(
            hall_address=self.hall_address,
            equipment=self.equipment,
        )

    def create_lecture(self):
        self.lecture = workrooms_models.Lecture.objects.create(
            name=self.name,
            svg=self.svg,
            optional=self.optional,
            type=self.type,
            listeners=self.listeners,
            cost=self.cost,
            description=self.description
        )

    def create_domain(self):
        if self.domain is not None:
            for name in self.domain:
                workrooms_models.LectureDomain.objects.create(
                    lecture=self.lecture,
                    domain=workrooms_models.Domain.objects.get(name=name)
                )

    def set_lecture_creator(self):
        if self._is_lecturer:
            self.lecture.lecturer = self.lecturer
        else:
            self.lecture.customer = self.customer

    def create_events(self):
        for event in self.datetime:
            lecture_request = workrooms_models.LectureRequest.objects.create(lecture=self.lecture)
            self.calendar.events.add(workrooms_models.Event.objects.create(
                datetime_start=event[0],
                datetime_end=event[1],
                lecture_request=lecture_request)
            )
        self.calendar.save()

    @transaction.atomic
    def create(self):
        self.create_optional()
        self.create_lecture()
        self.create_domain()
        self.set_lecture_creator()
        self.create_events()
        self.lecture.save()
        return self.lecture


class LectureEditor:
    updatable_fields = [
        'name',
        'domain',
        'listeners',
        'datetime',
        'hall_address',
        'equipment',
        'type',
        'cost',
        'description',
    ]

    def __init__(self, lecture, **kwargs):
        for field in self.updatable_fields:
            setattr(self, field, kwargs.get(field, None))

        self.lecture = lecture

    def update_lecture(self):
        lecture_attrs = {
            'name': self.name,
            'listeners': self.listeners,
            'type': self.type,
            'cost': self.cost or 0,
            'description': self.description or ''
        }
        not_null_attrs = {attr: lecture_attrs[attr] for attr in lecture_attrs if lecture_attrs[attr] is not None}

        for attr in not_null_attrs:
            setattr(self.lecture, attr, not_null_attrs[attr])

    def update_domain(self):
        if self.domain is not None:
            # удаляем существующие связанные тематики
            workrooms_models.LectureDomain.objects.filter(lecture=self.lecture).delete()

            for name in self.domain:
                # создаем новые
                workrooms_models.LectureDomain.objects.create(
                    lecture=self.lecture,
                    domain=workrooms_models.Domain.objects.get(name=name)
                )

    def update_optional(self):
        self.lecture.optional.hall_address = self.hall_address or ''
        self.lecture.optional.equipment = self.equipment or ''
        self.lecture.optional.save()

    def _get_calendar(self):
        if self.lecture.lecturer:
            return self.lecture.lecturer.lecturer_calendar.calendar
        return self.lecture.customer.customer_calendar.calendar

    def update_events(self):
        if self.datetime is not None:
            # удаляем все существующие даты лекции, чтобы не конфликтовали
            workrooms_models.LectureRequest.objects.filter(lecture=self.lecture).delete()
            calendar = self._get_calendar()

            for event in self.datetime:
                lecture_request = workrooms_models.LectureRequest.objects.create(lecture=self.lecture)
                calendar.events.add(workrooms_models.Event.objects.create(
                    datetime_start=event[0],
                    datetime_end=event[1],
                    lecture_request=lecture_request)
                )
            calendar.save()

    def update(self):
        self.update_lecture()
        self.update_domain()
        self.update_optional()
        self.update_events()
        self.lecture.save()
        return self.lecture


class LectureManager(models.Manager):
    def create_lecture(self, **kwargs):
        creator = LectureCreator(**kwargs)
        return creator.create()

    def update_lecture(self, lecture, **kwargs):
        updator = LectureEditor(lecture, **kwargs)
        return updator.update()
