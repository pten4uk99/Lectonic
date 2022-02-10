from drf_yasg.openapi import Schema

Unauthorized = Schema(
    title='',
    description='Пользователь успешно зарегистрирован',
    type='object',
    format='',
    enum=[],
    pattern='',
    properties={
        "user_profile": Schema(
            description='Возвращает email созданного пользователя',
            format='email',
            type='string',
            enum=['admin@yandex.ru']
        ),
        "status": Schema(
            description='Статус ответа',
            type='string',
            enum=['created']
        ),
    },
    required=[],
    default=None,
    read_only=None
)

GetLecturesSeccess = Schema(
    title='',
    description='Пользователь успешно зарегистрирован',
    type='object',
    format='',
    enum=[],
    pattern='',
    properties={
        "user_profile": Schema(
            description='Возвращает email созданного пользователя',
            format='email',
            type='string',
            enum=['admin@yandex.ru']
        ),
        "status": Schema(
            description='Статус ответа',
            type='string',
            enum=['created']
        ),
    },
    required=[],
    default=None,
    read_only=None
)

NoLecterueFound = Schema(
    title='',
    description='Пользователь успешно зарегистрирован',
    type='object',
    format='',
    enum=[],
    pattern='',
    properties={
        "user_profile": Schema(
            description='Возвращает email созданного пользователя',
            format='email',
            type='string',
            enum=['admin@yandex.ru']
        ),
        "status": Schema(
            description='Статус ответа',
            type='string',
            enum=['created']
        ),
    },
    required=[],
    default=None,
    read_only=None
)
