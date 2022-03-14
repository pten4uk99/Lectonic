from django.core import exceptions
from django.db import models, transaction

from workroomsapp import models as workrooms_models


class LectureManager(models.Manager):
    @transaction.atomic
    def create_as_lecturer(self, name: str, photo: object = None,
                           lecturer: object = None, datetime: object = None,
                           hall_address: str = None, equipment: str = None,
                           lecture_type: str = None, status: bool = None,
                           duration: int = None, cost: int = 0,
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
            optional=optional,
            type=lecture_type,
            status=status,
            duration=duration,
            cost=cost,
            description=description
        )

        if domain is not None:
            for domain_id in domain:
                workrooms_models.LectureDomain.objects.create(
                    lecture=lecture,
                    domain=workrooms_models.Domain.objects.get(pk=int(domain_id))
                )

        lecture_request = workrooms_models.LectureRequest.objects.create(lecture=lecture)

        event = workrooms_models.Event.objects.create(
            datetime=datetime, lecture_request=lecture_request)

        if lecturer.lecturer_calendar:
            calendar = lecturer.lecturer_calendar.calendar
            calendar.events.add(event)
            calendar.save()
        return workrooms_models.LecturerLectureRequest.objects.create(
            lecturer=lecturer,
            lecture_request=lecture_request,
            photo=photo
        )
