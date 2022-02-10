from drf_yasg.openapi import Schema

from authapp.utils import authapp_responses
from speakers.utils import response

UserProfileCreationSchema400 = Schema(
    title='',
    description='',
    type='object',
    format='',
    enum=[],
    pattern='',
    properties={
        "field": Schema(
            description='Описание ответа для пользователя',
            type='array',
            items=Schema(
                type='string'
            )
        )
    },
    required=[],
    default=None,
    read_only=None
)

UserProfileCreationSchema201 = Schema(
    title='Успешное создание пользователя',
    description='Пользователь содается и сразу авторизуется',
    type='object',
    format='',
    enum=[],
    pattern='',
    properties={
        "status": Schema(
            description='Статус ответа',
            type='string',
            enum=[response.SIGN_IN]
        ),
        "detail": Schema(
            description='Описание ответа для пользователя',
            type='string',
            enum=[authapp_responses.SIGNED_IN]
        ),
        "data": Schema(
            description='Возвращает email созданного пользователя',
            type='array',
            items=Schema(
                type='object',
                properties={
                    "user": Schema(type='string', enum=['admin@yandex.ru'])
                },
            ),
        ),
    },
    required=[],
    default=None,
    read_only=None
)

UserProfileLoginSchema200 = Schema(
    title='Успешная авторизация',
    type='object',
    format='',
    enum=[],
    pattern='',
    properties={
        "status": Schema(
            description='Статус ответа',
            type='string',
            enum=[response.LOGIN]
        ),
        "detail": Schema(
            description='Описание ответа для пользователя',
            type='string',
            enum=[authapp_responses.LOGGED_IN]
        ),
        "data": Schema(
            description='Пустой массив',
            type='string',
            enum=['[]']
        ),
    },
    required=[],
    default=None,
    read_only=None
)

UserProfileLoginSchema400 = Schema(
    title='Ошибка при авторизации',
    type='object',
    format='',
    enum=[],
    pattern='',
    properties={
        "field": Schema(
            description='Описание ответа для пользователя',
            type='array',
            items=Schema(
                type='string'
            )
        )
    },
    required=[],
    default=None,
    read_only=None
)
