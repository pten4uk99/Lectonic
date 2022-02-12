import csv
import os

from django.core.management import BaseCommand
from django.db import transaction

from speakers.settings import BASE_DIR
from workroomsapp.models import City, Domain, CompanyForm


class FileException(FileNotFoundError):
    pass


def load_cities():
    with open(os.path.join(BASE_DIR, 'db/ru_cities.csv'), encoding='utf-8') as f:
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
            print('Города успешно сохранены в базу данных...')


def load_domains():
    with open(os.path.join(BASE_DIR, 'db/domains.csv'), encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')

        with transaction.atomic():
            Domain.objects.all().delete()

            for domain in reader:
                Domain.objects.create(
                    name=domain[0]
                )
            print('Сферы деятельности успешно сохранены в базу данных...')


def load_forms():
    with open(os.path.join(BASE_DIR, 'db/company_forms.csv'), encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')

        with transaction.atomic():
            CompanyForm.objects.all().delete()

            for form in reader:
                CompanyForm.objects.create(
                    name=form[0]
                )
            print('Формы юрлица успешно сохранены в базу данных...')


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                load_cities()
                load_domains()
                load_forms()
        except FileNotFoundError:
            raise FileException('Чтобы команда выполнилась, необходимо поместить файлы '
                                f'ru_cities.csv '
                                f'в папку /db в корне проекта')
