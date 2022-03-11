from speakers.utils import response

PHOTO_CREATED = 'Фотография успешно загружена'
PHOTO_DOES_NOT_EXIST = 'Фотографий дипломов лектора не существует'
LECTURER_CREATED = 'Профиль лектора успешно создан'

DESCRIPTION = '\n\nВсе возможные статусы ответов:\n' \
              f'"{response.SUCCESS}"\n' \
              f'"{response.CREATE}"\n' \
              f'"{response.EMPTY}"\n' \
              f'"{response.ERROR}"'


def photo_created():
    return response.get_response(
        status=response.CREATE,
        detail=PHOTO_CREATED,
        status_code=201
    )


def lecturer_created():
    return response.get_response(
        status=response.CREATE,
        detail=LECTURER_CREATED,
        status_code=201
    )


def diploma_image_does_not_exist():
    return response.get_response(
        status=response.EMPTY,
        detail=PHOTO_DOES_NOT_EXIST,
        status_code=224
    )


def success(data):
    return response.get_response(
        status=response.SUCCESS,
        data=[data],
        status_code=200
    )
