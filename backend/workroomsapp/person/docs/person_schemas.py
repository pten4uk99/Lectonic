from drf_yasg.openapi import Schema

from config.utils import response
from config.utils.swagger_response import get_default_response
from workroomsapp.person import person_responses

DocumentImageCreationSchema = Schema(
    title='Загрузка фотографии для профиля пользователя',
    type='object',
    properties={
        'passport': Schema(
            type='string',
            format='byte',
            enum=['Тут должна быть фотография в байтах']
        ),
        'selfie': Schema(
            type='string',
            format='byte',
            enum=['Тут должна быть фотография в байтах']
        ),
    },
    required=['selfie', 'passport']
)

DocumentImageCreationSchema201 = Schema(
    title='Успешная загрузка фотографий',
    type='object',
    properties={
        **get_default_response(
            status=response.CREATE,
            detail=person_responses.PHOTO_CREATED
        ),
        "data": Schema(
            type='string',
            enum=['[]']
        ),
    },
)

DocumentImageCreationSchema400 = Schema(
    title='Ошибка в формате изображения',
    type='object',
    properties={
        "field_name": Schema(
            type='string',
            enum=['Паспорт/Селфи может быть только в формате "jpg", "jpeg" или "png"']
        ),
    },
)

DocumentImageGetSchema201 = Schema(
    title='Всё у вас получилось)',
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
                    'passport': Schema(
                        type='string',
                        enum=['https://dev.lectonic.ru/media/1010001/documents/1010001_passport.png']
                    ),
                    'selfie': Schema(
                        type='string',
                        enum=['https://dev.lectonic.ru/media/1010001/documents/1010001_selfie.png']
                    ),
                }
            )
        )
    },
)

DocumentImageGetSchema400 = Schema(
    title='Ничего у вас не вышло(',
    type='object',
    properties={
        **get_default_response(
            status=response.EMPTY,
            detail=person_responses.PHOTO_DOES_NOT_EXIST
        ),
        "data": Schema(
            type='string',
            enum=['[]']
        ),
    },
)

PersonCreationSchema = Schema(
    type='object',
    properties={
        "first_name": Schema(
            description='Имя',
            type='string',
            enum=['Пётр-Вадим']
        ),
        "last_name": Schema(
            description='Фамилия',
            type='string',
            enum=['Пётров-Вадимов']
        ),
        "middle_name": Schema(
            description='Отчество',
            type='string',
            enum=['Пётрович-Вадимович']
        ),
        "birth_date": Schema(
            description='Дата рождения',
            format='ГГГГ-ММ-ДД',
            type='string',
            enum=['1999-02-26']
        ),
        "city": Schema(
            description='ID города',
            type='number',
            enum=['871']
        ),
        "description": Schema(
            description='Описание',
            type='string',
            enum=['Это просто невероятное описание, какой же я классный.']
        ),
        "latitude": Schema(
            description='Можно вводить как целое, так и дробное число',
            type='number',
            enum=['50.0211349']
        ),
        "longitude": Schema(
            description='Можно вводить как целое, так и дробное число',
            type='number',
            enum=['50.0211349']
        ),
    },
    required=["first_name", "last_name", "birth_date", "city"],
)

PersonCreationSchema201 = Schema(
    title='Успешное создание базового профиля пользователя',
    type='object',
    properties={
        **get_default_response(
            status=response.CREATE,
            detail=person_responses.CREATED
        ),
        "data": Schema(
            description='Возвращает созданный объект в БД',
            type='array',
            items=Schema(
                type='object',
                properties={**PersonCreationSchema.properties, "city": Schema(type='string', enum=['Москва'])},
            ),
        ),
    },
)

PersonCreationSchema400 = Schema(
    title='Профиль уже существует',
    type='object',
    properties={
        **get_default_response(
            status=response.ERROR,
            detail=person_responses.IS_EXIST
        ),
        "data": Schema(
            type='string',
            enum=['[]']
        ),
    },
)

PersonGetSchema200 = Schema(
    title='Успешное получение данных профиля',
    type='object',
    properties={
        **get_default_response(
            status=response.SUCCESS,
        ),
        "data": Schema(
            description='Возвращает профиль текущего пользователя',
            type='array',
            items=Schema(
                type='object',
                properties={**PersonCreationSchema.properties, "city": Schema(type='string', enum=['Москва'])},
            ),
        )
    },
)

PersonGetSchema400 = Schema(
    title='Профиля для текущего пользователя не существует',
    type='object',
    properties={
        **get_default_response(
            status=response.ERROR,
            detail=person_responses.DONT_EXIST
        ),
        "data": Schema(
            type='string',
            enum=['[]']
        ),
    },
)

PersonPatchSchema200 = Schema(
    title='Данные профиля успешно изменены',
    type='object',
    properties={
        **get_default_response(
            status=response.SUCCESS,
            detail=person_responses.PATCHED
        ),
        "data": Schema(
            description='Возвращает новое значение измененного поля',
            type='array',
            items=Schema(
                type='object',
                properties={
                    "field": Schema(type='string')
                },
            ),
        ),
    },
)

PersonPatchSchema400 = Schema(
    title='Профиля для текущего пользователя не существует',
    type='object',
    properties={
        **get_default_response(
            status=response.ERROR,
            detail=person_responses.DONT_EXIST
        ),
        "data": Schema(
            type='string',
            enum=['[]']
        ),
    },
)

CityGetSchema200 = Schema(
    title='Список городов из базы',
    type='object',
    properties={
        **get_default_response(
            status=response.SUCCESS
        ),
        "data": Schema(
            type='array',
            items=Schema(
                type='object',
                properties={
                    'id': Schema(type='number', enum=['673']),
                    'name': Schema(type='string', enum=['Москва']),
                    'region': Schema(type='string', enum=['Московская область']),

                }
            )
        ),
    },
)

CityGetSchema224 = Schema(
    title='Совпадений по введенной части названия не найдено',
    type='object',
    properties={
        **get_default_response(
            status=response.EMPTY
        ),
        "data": Schema(
            type='string',
            enum=['[]']
        ),
    },
)

DomainGetSchema200 = Schema(
    title='Список тематик из базы',
    type='object',
    properties={
        **get_default_response(
            status=response.SUCCESS
        ),
        "data": Schema(
            type='array',
            items=Schema(
                type='object',
                properties={
                    'id': Schema(type='number', enum=['9']),
                    'name': Schema(type='string', enum=['Дизаин']),
                }
            )
        ),
    },
)