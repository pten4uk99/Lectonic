import datetime


def check_datetime_for_lecture(lecturer, date, time_start, time_end):
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

    for lecturer_lecture_request in lecturer.lecturer_lecture_request.all():
        events_today = lecturer_lecture_request.lecture_request.events.filter(datetime__range=(today_start, today_end))

        if events_today:
            for event in events_today:
                duration = event.lecture_request.lecture.duration

                if event.datetime <= start < (event.datetime + datetime.timedelta(minutes=duration)):
                    return False
                elif event.datetime < end < (event.datetime + datetime.timedelta(minutes=duration)):
                    return False
                elif (start < event.datetime and
                      end > (event.datetime + datetime.timedelta(minutes=duration))):
                    return False

    return True
