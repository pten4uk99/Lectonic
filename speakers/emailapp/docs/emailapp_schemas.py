from drf_yasg import openapi
from drf_yasg.openapi import Schema

EmailConfirmationCh1Error400 = Schema(
    type=openapi.TYPE_OBJECT,
    description='Запрос не выполнен',
    properties={
        'status': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Статус ответа',
            enum=[
                'error',
                ],
            ),
        'detail': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Описание ошибки',
            enum=[
                'В запросе нет электронной почты',
                'Отправить повторное письмо можно через 30 секунд',
                ],
            ),
        'data': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_STRING),
            description='Данные ответа',
            ),
        },
    )

EmailConfirmationCh2Error400 = Schema(
    type=openapi.TYPE_OBJECT,
    description='Запрос не выполнен',
    properties={
        'status': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Статус ответа',
            enum=[
                'error',
                ],
            ),
        'detail': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Описание ошибки',
            enum=[
                'Неверный ключ подтверждения электронной почты',
                'В запросе не передан код подтверждения',
                ],
            ),
        'data': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_STRING),
            description='Данные ответа',
            ),
        },
    )

EmailConfirmationCh1Success200 = Schema(
    type=openapi.TYPE_OBJECT,
    description='Запрос выполнен успешно',
    properties={
        'status': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Статус ответа',
            enum=[
                'success',
            ],
            ),
        'detail': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Описание',
            enum=[
                'На указанную электронную почту отправлено письмо подтверждения',
            ],
            ),
        'data': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_STRING),
            description='Данные ответа',
            ),
        },
    )

EmailConfirmationCh2Success200 = Schema(
    type=openapi.TYPE_OBJECT,
    description='Запрос выполнен успешно',
    properties={
        'status': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Статус ответа',
            enum=[
                'confirmed',
            ],
            ),
        'detail': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Описание',
            enum=[
                'Электронная почта успешно подтверждена',
            ],
            ),
        'data': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_EMAIL,
                enum=[
                    'test@lectonic.ru',
                ],
                ),
            description='Данные ответа',
            ),
        },
    )