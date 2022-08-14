from typing import NamedTuple, Type

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
    fields: list[FilterField] - поля по которым будет происходить фильтрация.
    ordering - поля для сортировки.

    Методы, которые можно переопределять:
    _default_filter_queryset() - если нужно изменить логику фильтрации по умолчанию с помощью переменных класса
    _filter() - если нужно изменить дополнительную логику фильтрации

    Использование:
    При создании экземпляра класса передать в него:
    1. qs: QuerySet - список, который будет фильтроваться. По умолчанию - список всех объектов self.model.
    1. from_obj: User - пользователь, для которого фильтруются объекты
    2. аргументы для фильтрации указанные в списке self.fields

    self.filter() - отфильтрует объекты.
    """
    
    queryset: QuerySet = None
    ordering: tuple[str] = ()

    def __init__(self, from_obj: User, qs: QuerySet = None, **kwargs):
        # пользователь, для которого происходит фильтрация
        self.from_obj = from_obj

        # сначала проходимся по переданным параметрам
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])
        
        if qs is not None:
            self.qs = self._default_filter_queryset(qs)
        else:
            self.qs = self.get_queryset()
            
    def get_queryset(self):
        assert self.queryset is not None, (
            '{} - не передан атрибут "queryset"'.format(self.__class__.__name__)
        )
        return self.queryset

    def _default_filter_queryset(self, qs: QuerySet = None) -> QuerySet:
        """ Возвращает полный список объектов """
        
        return qs.order_by(*self.ordering).distinct()

    def _filter(self) -> QuerySet:
        """ Выполняет логику по фильтрации. Фильтровать нужно self.qs """
        
        return self.qs

    def filter(self) -> QuerySet:
        """ Интерфейсный метод. Не рекомендуется переопределять. """

        return self._filter()


class FieldsFilter(BaseFilter):
    fields: list[FilterField] = None
    
    def __init__(self, from_obj: User, qs: QuerySet, **kwargs):
        super(FieldsFilter, self).__init__(from_obj, qs, **kwargs)
        
        assert self.fields is not None, 'Не передана обязательная переменная класса - fields'
        assert any(isinstance(x, FilterField) for x in self.fields), \
            'Элементы self.fields должны быть объектами FilterField'
        
    def _get_allowed_filters(self, fields: list[FilterField]) -> dict:
        """ Возвращает словарь только из ключей определенных в fields и переданных значений """

        filters = {}

        for field in fields:
            if hasattr(self, field.name) and getattr(self, field.name, False):
                filters[field.source] = getattr(self, field.name)

        return filters

    def _default_filter_queryset(self, qs: QuerySet = None) -> QuerySet:
        """ Возвращает полный список объектов """
    
        filters = self._get_allowed_filters(self.fields)
    
        qs = super()._default_filter_queryset(qs)
        return qs.filter(**filters)
    

class FilterBackend:
    """
    Пропускает self.qs через каждый из переданных self.filter_classes и
    возвращает отфильтрованный QuerySet
    """
    
    def __init__(self, from_obj: User, qs: QuerySet, filter_classes: list[Type[BaseFilter]], filter_query: dict = None):
        self.from_obj = from_obj
        self.qs = qs
        self.filter_classes = filter_classes
        
        self.filter_query = filter_query or {}
    
    @staticmethod
    def get_filter(qs: QuerySet, filter_class: Type[BaseFilter], from_obj: User, **kwargs) -> BaseFilter:
        """ Возвращает объект фильтра """
    
        return filter_class(qs=qs, from_obj=from_obj, **kwargs)

    def filter_queryset(self) -> QuerySet:
        queryset = self.qs
    
        for filter_class in self.filter_classes:
            filter_ = self.get_filter(queryset, filter_class, from_obj=self.from_obj, **self.filter_query)
            queryset = filter_.filter()
    
        return queryset
    
    