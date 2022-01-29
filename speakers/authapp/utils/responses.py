from speakers.utils import response


def created(data):
    return response.get_response(
        status=response.CREATED,
        detail='Пользователь успешно зарегистрирован',
        data=data,
        status_code=201
    )


def logged_in(cookie: tuple):
    return response.get_response(
        status=response.LOGIN,
        detail='Пользователь успешно авторизован',
        status_code=200,
        set_cookie=cookie
    )


def logged_out(cookie: str):
    return response.get_response(
        status=response.LOGOUT,
        detail='Пользователь успешно вышел из системы',
        status_code=200,
        delete_cookie=cookie
    )


def deleted(cookie: str):
    return response.get_response(
        status=response.DELETED,
        detail='Пользователь успешно удален',
        status_code=200,
        delete_cookie=cookie
    )