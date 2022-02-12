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
    'operation_description': 'Получение базового профиля для текущего пользователя. ' + DESCRIPTION,  # Развернутое описание
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
