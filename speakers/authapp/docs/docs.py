from authapp.serializers import UserCreateSerializer
from authapp.docs.schemas import *

UserProfileCreationView = {
    'request_body': UserCreateSerializer,  # Сериализатор
    'query_serializer': None,  # Пока что не совсем понял, что это но тоже сериализатор
    'manual_parameters': None,
    'operation_id': None,  # Меняет латинское название в snake_case справа, лучше не трогать
    'operation_description': 'Регистрация нового пользователя',  # Развернутое описание
    'operation_summary': 'Регистрация',  # Краткое описание
    'security': [],  # Должен быть какой то объект, пока не разобрался
    'deprecated': False,  # Если True, помечает API как не рабочее
    'responses': {
        201: UserProfileCreationSchema201,
        400: UserProfileCreationSchema400,
    },  # Схемы ответов сервера
    'field_inspectors': None,
    'filter_inspectors': None,
    'paginator_inspectors': None,
    'tags': None
}


UserProfileLoginView = {
    'method': None,
    'methods': None,
    'request_body': None,
    'query_serializer': None,
    'manual_parameters': None,
    'operation_id': None,
    'operation_description': 'partial_update description override',
    'operation_summary': None,
    'security': None,
    'deprecated': None,
    'responses': {404: 'slug not found'},
    'field_inspectors': None,
    'filter_inspectors': None,
    'paginator_inspectors': None,
    'tags': None
}


UserProfileLogoutView = {
    'method': None,
    'methods': None,
    'request_body': None,
    'query_serializer': None,
    'manual_parameters': None,
    'operation_id': None,
    'operation_description': 'partial_update description override',
    'operation_summary': None,
    'security': None,
    'deprecated': None,
    'responses': {404: 'slug not found'},
    'field_inspectors': None,
    'filter_inspectors': None,
    'paginator_inspectors': None,
    'tags': None
}

UserProfileDeleteView = {
    'method': None,
    'methods': None,
    'request_body': None,
    'query_serializer': None,
    'manual_parameters': None,
    'operation_id': None,
    'operation_description': 'partial_update description override',
    'operation_summary': None,
    'security': None,
    'deprecated': None,
    'responses': {404: 'slug not found'},
    'field_inspectors': None,
    'filter_inspectors': None,
    'paginator_inspectors': None,
    'tags': None
}
