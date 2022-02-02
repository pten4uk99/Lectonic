from speakers.utils import response

def validation_error(data):
    return response.get_response(
        status=response.ERROR,
        detail='Некоторые поля не прошли валидацию',
        data=[data],
        status_code=400
    )

def wrong_format():
    return response.get_response(
        status=response.ERROR,
        detail='Не верный формат переданных данных. Нет одного или нескольких обязательных параметров (например, id) или указаны лишние',
        status_code=400
    )

def created(data):
    return response.get_response(
        status=response.CREATE,
        detail='Запись добавлена успешно',
        data=[data],
        status_code=201
    )

def lecture_does_not_exist():
    return response.get_response(
        status=response.ERROR,
        detail='Такой лекции не существует',
        status_code=224
    )

def have_no_lectures():
    return response.get_response(
        status=response.ERROR,
        detail='У вас не добавлено ни одной лекции',
        status_code=224
    )

def operation_report(data):
    return response.get_response(
        status=response.ERROR,
        detail='Одна или несколько операций не была завершена успешно',
        data=[data],
        status_code=224
    )

def success_response(data):
    return response.get_response(
        status=response.SUCCESS,
        detail='Запрос выполнен успешно',
        data=[data],
        status_code=200
    )

def not_owner():
    return response.get_response(
        status=response.ERROR,
        detail='У вас нет прав для выполнения операции',
        status_code=403
    )