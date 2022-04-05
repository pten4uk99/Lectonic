import datetime


def convert_datetime(str_start, str_end):
    start = datetime.datetime.strptime(str_start, '%Y-%m-%dT%H:%M')
    end = datetime.datetime.strptime(str_end, '%Y-%m-%dT%H:%M')
    return start, end


def check_datetime_for_lecture_as_lecturer(lecturer, date, time_start, time_end):
    start = datetime.datetime(
        date.year,
        date.month,
        date.day,
        time_start.hour,
        time_start.minute,
        tzinfo=datetime.timezone.utc
    )
    end = datetime.datetime(
        date.year,
        date.month,
        date.day,
        time_end.hour,
        time_end.minute,
        tzinfo=datetime.timezone.utc
    )

    today_start = datetime.datetime(date.year, date.month, date.day, 0, 0)
    today_end = datetime.datetime(date.year, date.month, date.day, 23, 59)

    for lecturer_lecture_request_today in lecturer.lecturer_lecture_requests.filter(
            lecture_requests__event__datetime_start__range=(today_start, today_end)):
        lecture_request = lecturer_lecture_request_today.lecture_request

        if lecture_request.event.datetime_start <= start < lecture_request.event.datetime_end:
            return False
        elif lecture_request.event.datetime_start < end < lecture_request.event.datetime_end:
            return False
        elif start < lecture_request.event.datetime_start and end > lecture_request.event.datetime_end:
            return False

    return True


def check_datetime_for_lecture_as_customer(customer, date, time_start, time_end):
    start = datetime.datetime(
        date.year,
        date.month,
        date.day,
        time_start.hour,
        time_start.minute,
        tzinfo=datetime.timezone.utc
    )
    end = datetime.datetime(
        date.year,
        date.month,
        date.day,
        time_end.hour,
        time_end.minute,
        tzinfo=datetime.timezone.utc
    )

    today_start = datetime.datetime(date.year, date.month, date.day, 0, 0)
    today_end = datetime.datetime(date.year, date.month, date.day, 23, 59)

    for customer_lecture_request_today in customer.customer_lecture_requests.filter(
            lecture_request__event__datetime_start__range=(today_start, today_end)):
        lecture_request = customer_lecture_request_today.lecture_request

        if lecture_request.event.datetime_start <= start < lecture_request.event.datetime_end:
            return False
        elif lecture_request.event.datetime_start < end < lecture_request.event.datetime_end:
            return False
        elif start < lecture_request.event.datetime_start and end > lecture_request.event.datetime_end:
            return False

    return True
