from drf_yasg.openapi import Schema


def get_default_response(status: str = "", detail: str = ""):
    return {
        "status": Schema(
            description='Статус ответа',
            type='string',
            enum=[status]
        ),
        "detail": Schema(
            description='Описание ответа для пользователя',
            type='string',
            enum=[detail]
        ),
    }
