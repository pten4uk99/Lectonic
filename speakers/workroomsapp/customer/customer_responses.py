from speakers.utils import response

CUSTOMER_CREATED = 'Профиль заказчика успешно создан'
CUSTOMER_DOES_NOT_EXIST = 'Профиль заказчика не существует'

DESCRIPTION = '\n\nВсе возможные статусы ответов:\n' \
              f'"{response.SUCCESS}"\n' \
              f'"{response.CREATE}"\n' \
              f'"{response.EMPTY}"\n' \
              f'"{response.ERROR}"'


def customer_created():
    return response.get_response(
        status=response.CREATE,
        detail=CUSTOMER_CREATED,
        status_code=201
    )


def customer_does_not_exist():
    return response.get_response(
        status=response.ERROR,
        detail=CUSTOMER_DOES_NOT_EXIST,
        status_code=400
    )


def success_get_customer(data):
    return response.get_response(
        status=response.ERROR,
        data=data,
        status_code=200
    )
