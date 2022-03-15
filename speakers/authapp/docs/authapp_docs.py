from authapp.authapp_serializers import UserCreateSerializer, UserLoginSerializer
from authapp.docs.authapp_schemas import *
from authapp.utils.authapp_responses import DESCRIPTION

CheckAuthenticationDocs = {
    'operation_description': 'Проверка авторизован ли пользователь.',
    'operation_summary': 'Проверка авторизации',  # Краткое описание
    'deprecated': False,  # Если True, помечает API как не рабочее
    'responses': {
        200: CheckAuthenticationSchema200,
        400: CheckAuthenticationSchema400,
    },  # Схемы ответов сервера
}

UserProfileCreationView = {
    'request_body': UserCreateSerializer,  # Сериализатор
    'operation_description': 'Регистрация нового пользователя. ' + DESCRIPTION,  # Развернутое описание
    'operation_summary': 'Регистрация',  # Краткое описание
    'deprecated': False,  # Если True, помечает API как не рабочее
    'responses': {
        201: UserProfileCreationSchema201,
        400: UserProfileCreationSchema400,
    },  # Схемы ответов сервера
}


UserProfileLoginView = {
    'request_body': UserLoginSerializer,  # Сериализатор
    'operation_description': 'Пользователь авторизуется. '
                             'В браузер пользователя записывается кука с токеном, '
                             'которая автоматически передается с каждым запросом. ' + DESCRIPTION,  # Развернутое описание
    'operation_summary': 'Авторизация',  # Краткое описание
    'deprecated': False,  # Если True, помечает API как не рабочее
    'responses': {
        200: UserProfileLoginSchema200,
        400: UserProfileLoginSchema400,
    },  # Схемы ответов сервера
}


UserProfileLogoutView = {
    'operation_description': 'Из запроса забирается кука с токеном и логаутит пользователя. ' + DESCRIPTION,  # Развернутое описание
    'operation_summary': 'Выход из системы',  # Краткое описание
    'deprecated': False,  # Если True, помечает API как не рабочее
    'responses': {
        200: UserProfileLoginSchema200,
        400: UserProfileLoginSchema400,
    },  # Схемы ответов сервера
}

UserProfileDeleteView = {
    'operation_description': 'Пользователь должен быть авторизован. '
                             'Из запроса забирается кука с токеном и удаляет пользователя.',  # Развернутое описание
    'operation_summary': 'Удаление пользователя',  # Краткое описание
    'deprecated': False,  # Если True, помечает API как не рабочее
}
