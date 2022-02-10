from emailapp.emailapp_serializers import EmailConfirmationSerializer
from .emailapp_schemas import *


EmailConfirmationDocCh1 = {
    'request_body': EmailConfirmationSerializer,
    'query_serializer': None,
    'manual_parameters': None,
    'operation_id': None,
    'operation_summary': 'Подтверждение email часть 1',
    'operation_description': 'В этой части происходит отправка введенной почты на бэкенд для получения письма с кодом подтверждения',
    'deprecated': False,
    'responses': {
        200: EmailConfirmationCh1Success200,
        400: EmailConfirmationCh1Error400,
        },
    'field_inspectors': None,
    'filter_inspectors': None,
    'paginator_inspectors': None,
    'security': [],
    'tags': ['Администратор','Разработчик','Гость','Лектор','Компания','Слушатель','Арендодатель']
}

key = openapi.Parameter(
    'key',
    openapi.IN_QUERY,
    description="Код подтверждения",
    type=openapi.TYPE_STRING,
    required=True,
    )

EmailConfirmationDocCh2 = {
    'manual_parameters': [key],
    'operation_id': None,
    'operation_summary': 'Подтверждение email часть 2',
    'operation_description': 'В этой части происходит отправка ключа подтверждения в GET-запросе, который был выслан на почту',
    'deprecated': False,
    'responses': {
        200: EmailConfirmationCh2Success200,
        400: EmailConfirmationCh2Error400,
        },
    'field_inspectors': None,
    'filter_inspectors': None,
    'paginator_inspectors': None,
    'security': [],
    'tags': ['Администратор','Разработчик','Гость','Лектор','Компания','Слушатель','Арендодатель']
}