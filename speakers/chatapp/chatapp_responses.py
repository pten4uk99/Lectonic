from speakers.utils import response

CHAT_ID_NOT_IN_DATA = 'Параметр chat_id не передан'
CHAT_NOT_EXIST = 'Не найден чат с таким id'

DESCRIPTION = '\n\nВсе возможные статусы ответов:\n' \
              f'"{response.SUCCESS}"\n' \
              f'"{response.CREATE}"\n' \
              f'"{response.EMPTY}"\n' \
              f'"{response.ERROR}"'


def success(data):
    return response.get_response(
        status=response.SUCCESS,
        data=data,
        status_code=200
    )


def chat_id_not_in_data():
    return response.get_response(
        status=response.ERROR,
        detail=CHAT_ID_NOT_IN_DATA,
        status_code=200
    )


def chat_does_not_exist():
    return response.get_response(
        status=response.ERROR,
        detail=CHAT_NOT_EXIST,
        status_code=200
    )
