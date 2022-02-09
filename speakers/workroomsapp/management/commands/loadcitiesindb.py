import csv
import os

from django.core.management import BaseCommand
from django.db import transaction

from speakers.settings import BASE_DIR
from workroomsapp.models import City


class FileException(FileNotFoundError):
    pass


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            action='store'
        )

    def handle(self, *args, **options):
        try:
            with open(os.path.join(BASE_DIR, options.get('filename', 'ru_cities.csv')), encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=';')

                with transaction.atomic():
                    City.objects.all().delete()

                    for city in reader:
                        if city:
                            city_name = city[2]
                            city_region = city[3]

                            City.objects.create(
                                name=city_name,
                                region=city_region,
                                country='Россия'
                            )
        except FileNotFoundError:
            raise FileException('Чтобы команда выполнилась, необходимо поместить файл '
                  f'{options.get("filename", "ru_cities.csv")} '
                  f'рядом с файлом manage.py в папке /speakers/speakers')
