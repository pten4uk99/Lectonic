from speakers.utils import response

CUSTOMER_CREATED = 'Профиль заказчика успешно создан'

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
