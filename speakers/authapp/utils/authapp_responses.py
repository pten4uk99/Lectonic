from speakers.utils import response


def signed_in(data, cookie):
    return response.get_response(
        status=response.SIGN_IN,
        detail='Пользователь успешно зарегистрирован и авторизован',
        data=data,
        set_cookie=cookie,
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
        status=response.DELETE,
        detail='Пользователь успешно удален',
        status_code=200,
        delete_cookie=cookie
    )