from workroomsapp.lecture.docs.lecture_schemas import *
from workroomsapp.lecture.lecture_responses import DESCRIPTION

LectureAsLecturerCreateDoc = {
    'request_body': LectureAsLecturerCreationSchema,
    'operation_description': 'Создание лекции от имени лектора. Чтобы все получилось, нужно чтобы был создан '
                             'базовый профиль пользователя и профиль лектора. ' + DESCRIPTION,
    'operation_summary': 'Создание лекции',  # Краткое описание
    'deprecated': False,  # Если True, помечает API как не рабочее
    'responses': {
        201: LectureAsLecturerCreateSchema201,
        400: LectureAsLecturerCreateSchema400
    },
}