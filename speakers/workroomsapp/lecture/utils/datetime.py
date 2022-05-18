import datetime

import pytz


def convert_datetime(str_start, str_end):
    start = datetime.datetime.strptime(str_start, '%Y-%m-%dT%H:%M')
    end = datetime.datetime.strptime(str_end, '%Y-%m-%dT%H:%M')
    return start, end


def check_datetime_for_lecture(creator, dt_start, dt_end):
    today_start = datetime.datetime(dt_start.year, dt_start.month, dt_start.day, 0, 0)
    today_end = datetime.datetime(dt_start.year, dt_start.month, dt_start.day, 23, 59)

    for lecture in creator.lectures.filter(
            lecture_requests__event__datetime_start__range=(today_start, today_end)):

        for lecture_request in lecture.lecture_requests.all():

            if lecture_request.event.datetime_start <= dt_start < lecture_request.event.datetime_end:
                return False
            elif lecture_request.event.datetime_start < dt_end < lecture_request.event.datetime_end:
                return False
            elif dt_start < lecture_request.event.datetime_start and dt_end > lecture_request.event.datetime_end:
                return False

    return True

