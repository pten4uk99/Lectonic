from drf_yasg.openapi import Schema

from speakers.utils import response
from speakers.utils.swagger_response import get_default_response
from workroomsapp.utils.responses import person_responses


PersonCreationSchema = Schema(
    title='',
    description='',
    type='object',
    format='',
    enum=[],
    pattern='',
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
    default=None,
    read_only=None
)

PersonCreationSchema201 = Schema(
    title='Успешное создание базового профиля пользователя',
    description='',
    type='object',
    format='',
    enum=[],
    pattern='',
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
    required=[],
    default=None,
    read_only=None
)

PersonCreationSchema400 = Schema(
    title='Профиль уже существует',
    description='',
    type='object',
    format='',
    enum=[],
    pattern='',
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
    required=[],
    default=None,
    read_only=None
)

PersonGetSchema200 = Schema(
    title='Успешное получение данных профиля',
    description='',
    type='object',
    format='',
    enum=[],
    pattern='',
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
    required=[],
    default=None,
    read_only=None
)

PersonGetSchema400 = Schema(
    title='Профиля для текущего пользователя не существует',
    description='',
    type='object',
    format='',
    enum=[],
    pattern='',
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
    required=[],
    default=None,
    read_only=None
)

PersonPatchSchema200 = Schema(
    title='Данные профиля успешно изменены',
    description='',
    type='object',
    format='',
    enum=[],
    pattern='',
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
    required=[],
    default=None,
    read_only=None
)

PersonPatchSchema400 = Schema(
    title='Профиля для текущего пользователя не существует',
    description='',
    type='object',
    format='',
    enum=[],
    pattern='',
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
    required=[],
    default=None,
    read_only=None
)

CityGetSchema200 = Schema(
    title='Список городов из базы',
    description='',
    type='object',
    format='',
    enum=[],
    pattern='',
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
    required=[],
    default=None,
    read_only=None
)

CityGetSchema224 = Schema(
    title='Совпадений по введенной части названия не найдено',
    description='',
    type='object',
    format='',
    enum=[],
    pattern='',
    properties={
        **get_default_response(
            status=response.EMPTY
        ),
        "data": Schema(
            type='string',
            enum=['[]']
        ),
    },
    required=[],
    default=None,
    read_only=None
)
