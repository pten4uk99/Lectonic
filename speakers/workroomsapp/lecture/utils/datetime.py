from datetime import datetime
from typing import Union

from workroomsapp.models import Customer, Lecturer, LectureRequest


def _check_datetime_has_no_conflicts(lecture_request: LectureRequest,
                                     dt_start: datetime, dt_end: datetime) -> bool:
    """ Проверяет, не пересекаются ли dt_start и dt_end, с датой и временем lecture_request """

    if lecture_request.event.datetime_start <= dt_start < lecture_request.event.datetime_end:
        return False
    elif lecture_request.event.datetime_start < dt_end < lecture_request.event.datetime_end:
        return False
    elif dt_start < lecture_request.event.datetime_start and dt_end > lecture_request.event.datetime_end:
        return False

    return True


def check_datetime_for_lecture(creator: Union[Lecturer, Customer],
                               dt_start: datetime, dt_end: datetime) -> bool:
    """ Проверяет можно ли создать лекцию на выбранную дату """

    today_start = datetime(dt_start.year, dt_start.month, dt_start.day, 0, 0)
    today_end = datetime(dt_start.year, dt_start.month, dt_start.day, 23, 59)

    no_conflicts = True

    for lecture in creator.lectures.filter(
            lecture_requests__event__datetime_start__range=(today_start, today_end)):

        for lecture_request in lecture.lecture_requests.all():
            no_conflicts = _check_datetime_has_no_conflicts(lecture_request, dt_start, dt_end)

    return no_conflicts


def convert_datetime(str_start, str_end):
    start = datetime.strptime(str_start, '%Y-%m-%dT%H:%M')
    end = datetime.strptime(str_end, '%Y-%m-%dT%H:%M')
    return start, end
