from typing import NamedTuple

from django.db.models import QuerySet

from authapp.models import User


class FilterField(NamedTuple):
    """
    name - человеко читаемое имя, например: 'domain'
    source - путь до поля name в базе данных, например: 'lecture_domain__domain__name'
    """

    name: str
    source: str


class BaseFilter:
    """
    Базовый класс для фильтрации моделей базы данных.

    При наследовании:
    model: django.db.models.Model() - обязательный параметр. Объекты какой модели подлежат фильтрации.
    fields: list[FilterField] - поля по которым будет происходить фильтрация.
    ordering - поля для сортировки.

    Методы, которые можно переопределять:
    _default_filter_queryset() - если нужно изменить логику фильтрации по умолчанию с помощью переменных класса
    _filter() - если нужно изменить дополнительную логику фильтрации

    Использование:
    При создании экземпляра класса передать в него:
    1. from_obj: User - пользователь, для которого фильтруются объекты
    2. аргументы для фильтрации указанные в списке self.fields

    self.filter() - отфильтрует объекты.
    """

    model = None
    fields: list[FilterField] = None
    ordering: tuple[str] = ()

    def __init__(self, from_obj: User, **kwargs):
        # пользователь, для которого происходит фильтрация
        self.from_obj = from_obj

        # сначала проходимся по переданным параметрам
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])

        # даже если переменная класса не была передана, но в инициализатор передать аргумент model,
        # то к этому моменту self.model уже будет не None и ошибка не возникнет
        assert self.model is not None, 'Не передана обязательная переменная класса - model'
        assert self.fields is not None, 'Не передана обязательная переменная класса - fields'
        assert any(isinstance(x, FilterField) for x in self.fields), \
            'Элементы self.fields должны быть объектами FilterField'

        self.qs = self._default_filter_queryset()

    def _get_allowed_filters(self, fields: list[FilterField]) -> dict:
        """ Возвращает словарь только из ключей определенных в fields и переданных значений """

        filters = {}

        for field in fields:
            if hasattr(self, field.name) and getattr(self, field.name, False):
                filters[field.source] = getattr(self, field.name)

        return filters

    def _default_filter_queryset(self) -> QuerySet:
        """ Возвращает полный список объектов """

        filters = self._get_allowed_filters(self.fields)
        qs = self.model._default_manager.order_by(*self.ordering).filter(**filters).distinct()
        return qs

    def _filter(self) -> QuerySet:
        """ Выполняет логику по фильтрации. Фильтровать нужно self.qs """
        
        return self.qs

    def filter(self) -> QuerySet:
        """ Интерфейсный метод. Не рекомендуется переопределять. """

        return self._filter()

