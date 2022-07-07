from drf_yasg.openapi import Schema

from config.utils import response
from config.utils.swagger_response import get_default_response
from workroomsapp.lecture import lecture_responses

LectureAsLecturerCreationSchema = Schema(
    type='object',
    properties={
        "name": Schema(
            description='Название/тема лекции',
            type='string',
            enum=['Лекция Юрия Цезаря'],
        ),
        "domain": Schema(
            description='Тематика лекции',
            type='array',
            items=Schema(type='string', enum=['Генеалогия'])
        ),
        "photo": Schema(
            description='Фотография лекции',
            type='bytes',
            enum=['Фотография в байтах']
        ),
        "datetime": Schema(
            description='Назначенная дата и время лекции в формате: YYYY-MM-DDTHH:MM',
            type='string',
            enum=['2020-07-26T15:30']
        ),
        "duration": Schema(
            description='Длительность лекции в минутах',
            type='number',
            enum=['20']
        ),
        "cost": Schema(
            description='Стоимость лекции',
            type='number',
            enum=['2000']
        ),
        "lecture_type": Schema(
            description='Тип лекции. Всего три возможных варианта: "offline", "online", "hybrid"',
            type='string',
            enum=['offline']
        ),
        "hall_address": Schema(
            description='Адрес помещения для проведения лекции. Если нет, то ничего не отправлять.',
            type='string',
            enum=['Москва, ул. Не московская, д. Домашний']
        ),
        "equipment": Schema(
            description='Оборудование',
            type='string',
            enum=['Руки, ноги, доска, стол, стул.']
        ),
    },
    required=['name', 'photo', 'datetime', 'duration', 'lecture_type'],
)

LectureAsLecturerCreateSchema201 = Schema(
    title='Лекция успешно создана',
    type='object',
    properties={
        **get_default_response(
            status=response.CREATE,
            detail=lecture_responses.LECTURE_CREATED
        ),
        "data": Schema(
            type='string',
            enum=['[]']
        ),
    },
)

LectureAsLecturerCreateSchema400 = Schema(
    title='Ошибка валидации',
    type='object',
    properties={
        "detail": Schema(type='string'),
    },
)