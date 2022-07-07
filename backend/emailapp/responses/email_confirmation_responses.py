from config.utils import response


def mail_is_sent():
    return response.get_response(
        status=response.SUCCESS,
        detail='На указанную электронную почту отправлено письмо подтверждения',
        status_code=200
    )


def confirmed(data):
    return response.get_response(
        status=response.CONFIRM,
        detail='Электронная почта успешно подтверждена',
        data=data,
        status_code=200
    )


def user_is_exist():
    return response.get_response(
        status=response.ERROR,
        detail='Пользователь с таким e-mail уже зарегистрирован',
        status_code=400
    )


def bad_key():
    return response.get_response(
        status=response.ERROR,
        detail='Неверный ключ подтверждения электронной почты',
        status_code=400
    )


def email_not_in_data():
    return response.get_response(
        status=response.ERROR,
        detail='В запросе нет электронной почты',
        status_code=400
    )


def key_not_in_get():
    return response.get_response(
        status=response.ERROR,
        detail='В запросе не передан код подтверждения',
        status_code=400
    )


def can_not_repeat_confirmation():
    return response.get_response(
        status=response.ERROR,
        detail='Отправить повторное письмо можно через 30 секунд',
        status_code=400
    )
