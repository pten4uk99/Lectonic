from typing import Type

from django.db.models import QuerySet
from rest_framework.serializers import Serializer

from authapp.models import User
from services.filters.base import BaseFilter, FilterBackend
from utils import response


class ResponseMixin:
    """ Предоставляет методы для получения объекта ответа и ошибки """
    
    def get_error(self, detail: str = 'Ошибка запроса', status_code: int = 400):
        """ Возвращает исключение, которое можно выбросить через raise """
        
        return response.ErrorException(detail=detail, status_code=status_code)
    
    def get_response(self, status: str = response.SUCCESS, data: list = None,
                     detail: str = 'Успешно', status_code: int = 201):
        return response.get_response(
            status=status,
            data=data,
            detail=detail,
            status_code=status_code
        )


class QueryParamsMixin:
    """ Добавляет параметры адресной строки в представление """
    
    query_serializer_class: Type[Serializer] = None
    
    def __init__(self, *args, **kwargs):
        self.request = None
        super().__init__(*args, **kwargs)
    
    def get_error(self, *args, **kwargs):
        raise NotImplementedError()
    
    def get_query_serializer_class(self):
        return self.query_serializer_class
    
    def get_query(self) -> dict:
        """
        Проверяет корректность переданных параметров и возвращает словарь,
        который содержит параметры адресной строки.
        """
        
        serializer_class = self.get_query_serializer_class()
        serializer = serializer_class(data=self.request.GET)
        
        if not serializer.is_valid():
            raise self.get_error(detail='Не переданы необходимые параметры адресной строки')
        
        return serializer.data


class FilterMixin:
    """ Добавляет возможность фильтрации объектов в представление """
    
    filter_classes: list[Type[BaseFilter]] = None
    queryset: QuerySet = None
    
    def get_from_obj(self) -> User:
        raise NotImplementedError()
    
    def get_query(self) -> dict:
        raise NotImplementedError()
    
    def get_filter_classes(self):
        assert self.filter_classes is not None, (
            '{} объект должен содержать "filter_classes" атрибут'.format(self.__class__.__name__)
        )
        return self.filter_classes
    
    def get_filter(self, qs: QuerySet, filter_class: Type[BaseFilter], from_obj: User, **kwargs) -> BaseFilter:
        """ Возвращает объект фильтра """

        return filter_class(qs=qs, from_obj=from_obj, **kwargs)
    
    def filter_queryset(self, qs: QuerySet):
        filter_backend = FilterBackend(
            from_obj=self.get_from_obj(),
            qs=qs,
            filter_classes=self.get_filter_classes(),
            filter_query=self.get_query()
        )
            
        return filter_backend.filter_queryset()
    
    def get_queryset(self) -> QuerySet:
        assert self.queryset is not None, (
            '{} объект должен содержать "queryset" атрибут'.format(self.__class__.__name__)
        )
        
        qs = self.queryset
        return self.filter_queryset(qs)


class ResponseQueryFilterMixin(ResponseMixin,
                               QueryParamsMixin,
                               FilterMixin):
    pass
