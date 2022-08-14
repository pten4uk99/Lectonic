from utils import response

PHOTO_CREATED = 'Фотографии успешно загружены'
PHOTO_DOES_NOT_EXIST = 'Фотографий для данного профиля не существуют'
CREATED = 'Профиль пользователя успешно создан'
PATCHED = 'Профиль пользователя успешно изменен'
DONT_EXIST = 'Данного профиля не существует'
IS_EXIST = 'Профиль для текущего пользователя уже существует'

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


def document_image_does_not_exist():
    return response.get_response(
        status=response.EMPTY,
        detail=PHOTO_DOES_NOT_EXIST,
        status_code=224
    )


def created(data):
    return response.get_response(
        status=response.CREATE,
        detail=CREATED,
        data=data,
        status_code=201
    )


def patched(data):
    return response.get_response(
        status=response.SUCCESS,
        detail=PATCHED,
        data=data,
        status_code=200
    )


def success(data):
    return response.get_response(
        status=response.SUCCESS,
        data=data,
        status_code=200
    )


def empty():
    return response.get_response(
        status=response.EMPTY,
        status_code=224
    )


def no_data_in_request():
    return response.get_response(
        status=response.ERROR,
        detail='Не передано данных для изменения профиля',
        status_code=400
    )


def profile_does_not_exist():
    return response.get_response(
        status=response.ERROR,
        detail=DONT_EXIST,
        status_code=400
    )


def profile_is_existing():
    return response.get_response(
        status=response.ERROR,
        detail=IS_EXIST,
        status_code=400
    )
