from workroomsapp.serializers.lector_serializers import *
from workroomsapp.docs.lector_schemas import *

# UserProfileCreationView = {
#     'request_body': UserCreateSerializer,  # Сериализатор
#     'query_serializer': None,  # Пока что не совсем понял, что это но тоже сериализатор
#     'manual_parameters': None,
#     'operation_id': None,  # Меняет латинское название в snake_case справа, лучше не трогать
#     'operation_description': 'Регистрация нового пользователя',  # Развернутое описание
#     'operation_summary': 'Регистрация',  # Краткое описание
#     'security': [],  # Должен быть какой то объект, пока не разобрался
#     'deprecated': False,  # Если True, помечает API как не рабочее
#     'responses': {
#         201: UserProfileCreationSchema201,
#         400: UserProfileCreationSchema400,
#     },  # Схемы ответов сервера
#     'field_inspectors': None,
#     'filter_inspectors': None,
#     'paginator_inspectors': None,
#     'tags': None
# }

GetLectorLecturesDescribe = {
    'request_body': None,
    'query_serializer': None,
    'manual_parameters': None,
    'operation_id': None,
    'operation_description': 'Если в гет запросе передаётся параметр id, то в ответе получим данные лекции с этим id. Если гет запрос без параметров, то получим все активные (не удаленные, aka не архивные) лекции залогиненого лектора',
    'operation_summary': 'Получить все активные лекции залогиненого лектора или лекцию по id',
    'security': None,
    'deprecated': None,
    'responses': {
        200: GetLecturesSeccess,
        224: NoLecterueFound,
        401: Unauthorized,
    },
    'field_inspectors': None,
    'filter_inspectors': None,
    'paginator_inspectors': None,
    'tags': None
}
