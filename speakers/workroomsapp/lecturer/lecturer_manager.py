from django.core import exceptions
from django.db import models, transaction

from workroomsapp import models as workrooms_models


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
            for name in domain:
                workrooms_models.LecturerDomain.objects.create(
                    lecturer=lecturer,
                    domain=workrooms_models.Domain.objects.get(name=name)
                )

        if performances_links is not None:
            for perf_link in performances_links:
                lecturer.performances_links.add(workrooms_models.Link.objects.create(url=perf_link))
        if publication_links is not None:
            for pub_link in publication_links:
                lecturer.publication_links.add(workrooms_models.Link.objects.create(url=pub_link))

        if diploma_image:
            for image in diploma_image:
                workrooms_models.DiplomaImage.objects.create(
                    lecturer=lecturer,
                    image=workrooms_models.Image.objects.create(photo=image))
        lecturer.save()

        calendar = workrooms_models.Calendar.objects.create()
        workrooms_models.LecturerCalendar.objects.create(
            lecturer=lecturer, calendar=calendar)

        person.is_lecturer = True
        person.save()

        return lecturer
