from workroomsapp.customer.customer_responses import DESCRIPTION
from workroomsapp.customer.docs.customer_schemas import *

CustomerCreateDoc = {
    'request_body': CustomerCreationSchema,
    'operation_description': 'Создание профиля заказчика(физлицо). Чтобы все получилось, нужно чтобы был создан '
                             'базовый профиль пользователя. ' + DESCRIPTION,
    'operation_summary': 'Создание профиля заказчика(физлицо)',  # Краткое описание
    'deprecated': False,  # Если True, помечает API как не рабочее
    'responses': {
        201: CustomerCreationSchema201,
        400: CustomerCreationSchema400
    },
}