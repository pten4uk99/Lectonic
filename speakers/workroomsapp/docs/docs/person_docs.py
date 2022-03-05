from drf_yasg import openapi

from workroomsapp.docs.schemas.person_schemas import *
from workroomsapp.serializers.person_serializers import PersonSerializer
from workroomsapp.utils.responses.person_responses import DESCRIPTION

PersonCreationView = {
    'request_body': PersonCreationSchema,  # Сериализатор
    'operation_description': 'Создание нового базового профиля для текущего пользователя. ' + DESCRIPTION,  # Развернутое описание
    'operation_summary': 'Создание базового профиля',  # Краткое описание
    'deprecated': False,  # Если True, помечает API как не рабочее
    'responses': {
        201: PersonCreationSchema201,
        400: PersonCreationSchema400,
    },  # Схемы ответов сервера
}

PersonGetView = {
    'operation_description': 'Получение базового профиля для текущего пользователя. ' + DESCRIPTION,  # Развернутое описание
    'operation_summary': 'Получение базового профиля',  # Краткое описание
    'deprecated': False,  # Если True, помечает API как не рабочее
    'responses': {
        200: PersonGetSchema200,
        400: PersonGetSchema400,
    },  # Схемы ответов сервера
}

PersonPatchView = {
    'request_body': PersonCreationSchema,  # Сериализатор
    'operation_description': 'Получение базового профиля для текущего пользователя. ' + DESCRIPTION,
    'operation_summary': 'Получение базового профиля',  # Краткое описание
    'deprecated': False,  # Если True, помечает API как не рабочее
    'responses': {
        200: PersonPatchSchema200,
        400: PersonPatchSchema400,
    },  # Схемы ответов сервера
}

city_name = openapi.Parameter(
    'name',
    openapi.IN_QUERY,
    description="Название/часть названия города",
    type=openapi.TYPE_STRING,
    required=True,
)

DocumentImageCreateView = {
    'request_body': DocumentImageCreationSchema,
    'operation_description': 'Загрузка фотографий документов для лектора или заказчика. '
                             'Чтобы все успешно загрузилось, нужно создать базовый профиль. ' + DESCRIPTION,
    'operation_summary': 'Загрузка документов',  # Краткое описание
    'deprecated': False,  # Если True, помечает API как не рабочее
    'responses': {
        201: DocumentImageCreationSchema201,
        400: DocumentImageCreationSchema400
    },
}

DocumentImageGetView = {
    'operation_description': 'Получение ссылок фотографий документов для лектора или заказчика. ' + DESCRIPTION,
    'operation_summary': 'Получение фотографий документов',  # Краткое описание
    'deprecated': False,  # Если True, помечает API как не рабочее
    'responses': {
        200: DocumentImageGetSchema201,
        400: DocumentImageGetSchema400
    },  # Схемы ответов сервера
}

CityGetView = {
    'manual_parameters': [city_name],
    'operation_description': 'Получение списка городов по введенной части названия. ' + DESCRIPTION,  # Развернутое описание
    'operation_summary': 'Список городов',  # Краткое описание
    'deprecated': False,  # Если True, помечает API как не рабочее
    'responses': {
        200: CityGetSchema200,
        224: CityGetSchema224
    },  # Схемы ответов сервера
}
