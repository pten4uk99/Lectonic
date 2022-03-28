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

    for lecturer_lecture_request in lecturer.lecturer_lecture_requests.all():
        events_today = lecturer_lecture_request.lecture_request.events.filter(
            datetime_start__range=(today_start, today_end))

        if events_today:
            for event in events_today:

                if event.datetime_start <= start < event.datetime_end:
                    return False
                elif event.datetime_start < end < event.datetime_end:
                    return False
                elif start < event.datetime_start and end > event.datetime_end:
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

    for customer_lecture_request in customer.customer_lecture_requests.all():
        events_today = customer_lecture_request.lecture_request.events.filter(
            datetime_start__range=(today_start, today_end))

        if events_today:
            for event in events_today:

                if event.datetime_start <= start < event.datetime_end:
                    return False
                elif event.datetime_start < end < event.datetime_end:
                    return False
                elif start < event.datetime_start and end > event.datetime_end:
                    return False

    return True
