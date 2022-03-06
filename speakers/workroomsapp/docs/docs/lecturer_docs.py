from workroomsapp.docs.schemas.lecturer_schemas import *
from workroomsapp.utils.responses.lecturer_responses import DESCRIPTION

DiplomaImageCreateDoc = {
    'request_body': DiplomaImageCreationSchema,
    'operation_description': 'Загрузка фотографии дипломов лектора. '
                             'Чтобы все успешно загрузилось, '
                             'нужно чтобы у вас был создан профиль лектора. '
                             'Пока что возможно загрузить только одну фотографию. ' + DESCRIPTION,
    'operation_summary': 'Загрузка дипломов лектора',  # Краткое описание
    'deprecated': False,  # Если True, помечает API как не рабочее
    'responses': {
        201: DiplomaImageCreationSchema201,
        400: DiplomaImageCreationSchema400
    },
}

DiplomaImageGetDoc = {
    'operation_description': 'Получение ссылок фотографий дипломов для лектора. ' + DESCRIPTION,
    'operation_summary': 'Получение фотографий дипломов',  # Краткое описание
    'deprecated': False,  # Если True, помечает API как не рабочее
    'responses': {
        200: DiplomaImageGetSchema201,
        400: DiplomaImageGetSchema400
    },
}

LecturerCreateDoc = {
    'request_body': LecturerCreationSchema,
    'operation_description': 'Создание профиля лектора. Чтобы все получилось, нужно чтобы был создан '
                             'базовый профиль пользователя. ' + DESCRIPTION,
    'operation_summary': 'Создание профиля лектора',  # Краткое описание
    'deprecated': False,  # Если True, помечает API как не рабочее
    'responses': {
        201: LecturerCreationSchema201,
        400: LecturerCreationSchema400
    },
}