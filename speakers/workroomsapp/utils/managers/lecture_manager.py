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
