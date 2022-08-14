from drf_yasg.openapi import Schema

from utils import response
from utils.swagger import get_default_response
from workroomsapp.customer import customer_responses

CustomerCreationSchema = Schema(
    type='object',
    properties={
        "domain": Schema(
            description='Список выбранных тематик лекций',
            type='array',
            items=Schema(type='number', enum=['15']),
        ),
        "hall_address": Schema(
            description='Адрес помещения для проведения лекции. Если нет, то ничего не отправлять.',
            type='string',
            enum=['Москва, ул. Не московская, д. Домашний']
        ),
        "equipment": Schema(
            description='Оборудование',
            type='string',
            enum=['Руки, ноги, доска, стол, стул.']
        ),
    },
    required=[],
)

CustomerCreationSchema201 = Schema(
    title='Профиль заказчика успешно создан',
    type='object',
    properties={
        **get_default_response(
            status=response.CREATE,
            detail=customer_responses.CUSTOMER_CREATED
        ),
        "data": Schema(
            type='string',
            enum=['[]']
        ),
    },
)

CustomerCreationSchema400 = Schema(
    title='Ошибка валидации',
    type='object',
    properties={
        "detail": Schema(type='string'),
    },
)