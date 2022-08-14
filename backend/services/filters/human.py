from django.db.models import QuerySet

from services.filters.base import FieldsFilter
from workroomsapp.models import Lecturer, Customer
from .fields import LECTURER_FILTER_FIELDS, CUSTOMER_FILTER_FIELDS

__all__ = [
    'HumanFilter',
    'LecturerFilter',
    'CustomerFilter'
]


class HumanFilter(FieldsFilter):
    """
    Класс для фильтрации сторон взаимодействия на сервисе (Лектор, Заказчик...).
    """
    
    # этот метод можно будет убрать, когда будем менять базу
    def _build_exclude_dict(self) -> dict:
        """ Выстраивает словарь, в котором ключ - путь, используя ORM, к пользователю от текущей модели.
        А значение - сам пользователь """
        
        query_string = 'person__user'
        return {query_string: self.from_obj}
    
    def _filter(self) -> QuerySet:
        qs = super()._filter()
        exclude = self._build_exclude_dict()
        return qs.exclude(**exclude)


class LecturerFilter(HumanFilter):
    queryset = Lecturer.objects.all()
    fields = LECTURER_FILTER_FIELDS


class CustomerFilter(HumanFilter):
    queryset = Customer.objects.all()
    fields = CUSTOMER_FILTER_FIELDS
