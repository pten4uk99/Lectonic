from datetime import datetime, timedelta
from typing import Union, NamedTuple

from rest_framework import serializers

from workroomsapp.models import Lecturer, Customer, LectureRequest


class LectureDatetime(NamedTuple):
    start: datetime
    end: datetime


class LectureDatetimeValidator:
    # самая ранняя дата, на которую можно создать лекцию
    earliest_lecture_date: datetime = datetime.now() + timedelta(hours=1)

    def __init__(self, creator: Union[Lecturer, Customer], edit: bool = False):
        self.creator = creator
        self.edit = edit

    @staticmethod
    def _convert_datetime(str_start: str, str_end: str) -> LectureDatetime:
        start = datetime.strptime(str_start, '%Y-%m-%dT%H:%M')
        end = datetime.strptime(str_end, '%Y-%m-%dT%H:%M')
        return LectureDatetime(start=start, end=end)

    @staticmethod
    def _check_datetime_has_no_conflicts(lecture_request: LectureRequest,
                                         dt_start: LectureDatetime.start,
                                         dt_end: LectureDatetime.end) -> bool:
        """ Проверяет, не пересекаются ли dt_start и dt_end, с датой и временем lecture_request """

        if lecture_request.event.datetime_start <= dt_start < lecture_request.event.datetime_end:
            return False
        elif lecture_request.event.datetime_start < dt_end < lecture_request.event.datetime_end:
            return False
        elif dt_start < lecture_request.event.datetime_start and dt_end > lecture_request.event.datetime_end:
            return False

        return True

    def _check_conflict_with_other_lectures(self, dt_start: LectureDatetime.start,
                                            dt_end: LectureDatetime.end) -> bool:
        """ Проверяет можно ли создать лекцию на выбранную дату """

        today_start = datetime(dt_start.year, dt_start.month, dt_start.day, 0, 0)
        today_end = datetime(dt_start.year, dt_start.month, dt_start.day, 23, 59)

        no_conflicts = True

        for lecture in self.creator.lectures.filter(
                lecture_requests__event__datetime_start__range=(today_start, today_end)):

            for lecture_request in lecture.lecture_requests.all():
                no_conflicts = self._check_datetime_has_no_conflicts(lecture_request, dt_start, dt_end)

        return no_conflicts

    def _check_past_lecture_date(self, date: datetime) -> bool:
        """ Проверяет не раньше ли дата самой ближайшей разрешенной """

        return date > self.earliest_lecture_date

    @staticmethod
    def _check_dates_not_extended_more_than_one_day(
            start: LectureDatetime.start, end: LectureDatetime.end) -> bool:
        """ Проверяет не захватывают ли даты больше одного дня.
        Например начало лекции на 11 вечера одного дня,
        а конец на 2 часа ночи другого дня. """

        return start.day == end.day

    def _is_allowed(self, start: LectureDatetime.start, end: LectureDatetime.end) -> None:
        """ Производит все проверки валидации для конкретных start и end.
        Выбрасывает исключение, если какая-то из проверок не прошла. """

        if not self._check_conflict_with_other_lectures(start, end):
            msg = f'Событие на выбранное время уже существует {start} - {end}'
            if not self.edit:
                raise serializers.ValidationError(msg)

        if not self._check_past_lecture_date(start):
            msg = 'Невозможно создать событие на прошедшую дату'
            raise serializers.ValidationError(msg)

        if not self._check_dates_not_extended_more_than_one_day(start, end):
            msg = 'Невозможно создать событие, время которого выходит за пределы одного дня'
            raise serializers.ValidationError(msg)

    def validate(self, datetime_list: list[str]) -> list[LectureDatetime]:
        """ Метод для взаимодействия с классом извне, выполняет всю необходимую валидацию переданных дат """

        dates = []

        for elem in datetime_list:
            start, end = elem.split(',')
            start, end = self._convert_datetime(start, end)

            self._is_allowed(start, end)

            dates.append(LectureDatetime(start=start, end=end))

        return dates
