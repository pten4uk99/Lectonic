from speakers.utils import response

def success_response(data):
    return response.get_response(
        status=response.SUCCESS,
        detail='Запрос выполнен успешно',
        data=[data],
        status_code=200
    )

def have_no_lectures():
    return response.get_response(
        status=response.ERROR,
        detail='В БД не добавлено ни одной лекции',
        status_code=224
    )

def have_no_lecturers():
    return response.get_response(
        status=response.ERROR,
        detail='В БД не добавлено ни одного лектора',
        status_code=224
    )

def lecture_does_not_exist():
    return response.get_response(
        status=response.ERROR,
        detail='Такой лекции не существует',
        status_code=224
    )

def lecturer_does_not_exist():
    return response.get_response(
        status=response.ERROR,
        detail='Такого лектора не существует',
        status_code=224
    )

def wrong_format():
    return response.get_response(
        status=response.ERROR,
        detail='Параметр в get запросе должен быть целым числом больше 0',
        status_code=400
    )