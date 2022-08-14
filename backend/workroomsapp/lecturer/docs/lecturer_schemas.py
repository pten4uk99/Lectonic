from drf_yasg.openapi import Schema

from utils import response
from utils.swagger import get_default_response
from workroomsapp.lecturer import lecturer_responses

DiplomaImageCreationSchema = Schema(
    title='Загрузка фотографии для профиля пользователя',
    type='object',
    properties={
        'diploma': Schema(
            type='string',
            format='byte',
            enum=['Тут должна быть фотография в байтах']
        ),
    },
    required=['diploma']
)

DiplomaImageCreationSchema201 = Schema(
    title='Успешная загрузка фотографии',
    type='object',
    properties={
        **get_default_response(
            status=response.CREATE,
            detail=lecturer_responses.PHOTO_CREATED
        ),
        "data": Schema(
            type='string',
            enum=['[]']
        ),
    },
)

DiplomaImageCreationSchema400 = Schema(
    title='Ошибка в формате изображения',
    type='object',
    properties={
        "diploma": Schema(
            type='string',
            enum=['Диплом может быть только в формате "jpg", "jpeg" или "png"']
        ),
    },
)


DiplomaImageGetSchema201 = Schema(
    title='Успешное получение ссылок на фотографию',
    type='object',
    properties={
        **get_default_response(
            status=response.SUCCESS,
        ),
        'data': Schema(
            type='array',
            items=Schema(
                type='object',
                properties={
                    'diploma': Schema(
                        type='string',
                        enum=['https://dev.lectonic.ru/media/1010001/diploma/1010001_diploma.png']
                    ),
                }
            )
        )
    },
)

DiplomaImageGetSchema400 = Schema(
    title='Фотографии дипломов для данного профиля не найдены',
    type='object',
    properties={
        **get_default_response(
            status=response.EMPTY,
            detail=lecturer_responses.PHOTO_DOES_NOT_EXIST
        ),
        "data": Schema(
            type='string',
            enum=['[]']
        ),
    },
)

LecturerCreationSchema = Schema(
    type='object',
    properties={
        "domain": Schema(
            description='Список выбранных тематик лекций',
            type='array',
            items=Schema(type='string', enum=['Генеалогия']),
        ),
        "performances_links": Schema(
            description='Список ссылок на выступления',
            type='array',
            items=Schema(type='string', enum=['https://dev.lectonic.ru/performances'])
        ),
        "publication_links": Schema(
            description='Список ссылок на публикации',
            type='array',
            items=Schema(type='string', enum=['https://dev.lectonic.ru/publications'])
        ),
        "education": Schema(
            description='Образование',
            type='string',
            enum=['У меня 10 высших по ядерной физике и энергетикам.']
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
    required=[],
)

LecturerCreationSchema201 = Schema(
    title='Профиль лектора успешно создан',
    type='object',
    properties={
        **get_default_response(
            status=response.CREATE,
            detail=lecturer_responses.LECTURER_CREATED
        ),
        "data": Schema(
            type='string',
            enum=['[]']
        ),
    },
)

LecturerCreationSchema400 = Schema(
    title='Ошибка валидации',
    type='object',
    properties={
        "detail": Schema(type='string'),
    },
)