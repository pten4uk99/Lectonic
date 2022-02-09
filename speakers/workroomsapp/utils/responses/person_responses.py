from speakers.utils import response


def created(data):
    return response.get_response(
        status=response.CREATE,
        data=[data],
        status_code=201
    )


def success(data):
    return response.get_response(
        status=response.SUCCESS,
        data=[data],
        status_code=200
    )


def empty():
    return response.get_response(
        status=response.EMPTY,
        status_code=224
    )


def profile_does_not_exist():
    return response.get_response(
        status=response.ERROR,
        detail='Данного профиля не существует',
        status_code=224
    )


def profile_is_existing():
    return response.get_response(
        status=response.ERROR,
        detail='Профиль для текущего пользователя уже существует',
        status_code=400
    )
