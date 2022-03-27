from speakers.utils import response

LECTURE_CREATED = 'Лекция успешно создана'

DESCRIPTION = '\n\nВсе возможные статусы ответов:\n' \
              f'"{response.SUCCESS}"\n' \
              f'"{response.CREATE}"\n' \
              f'"{response.EMPTY}"\n' \
              f'"{response.ERROR}"'


def lecture_created():
    return response.get_response(
        status=response.CREATE,
        detail=LECTURE_CREATED,
        status_code=201
    )