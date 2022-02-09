from drf_yasg.openapi import Schema

UserProfileCreationSchema400 = Schema(
    title='',
    description='',
    type='object',
    format='',
    enum=[],
    pattern='',
    properties={
        "email": Schema(
            # title='',
            description='Пользователь с таким email уже существует',
            type='string',
            # format='',  # Формат данных
            enum=['пользователь с таким email уже существует'],  # Можно считать это вариантами ответа
            # pattern='',
            # properties=None, # Если type='object' то нужно задать это свойство
            # required=[],
            # default='',
            # read_only=None
        )
    },
    required=[],
    default=None,
    read_only=None
)

UserProfileCreationSchema201 = Schema(
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