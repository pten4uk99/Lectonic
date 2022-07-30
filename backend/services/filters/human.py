from services.filters.base import BaseFilter
from .fields import LECTURER_FILTER_FIELDS, CUSTOMER_FILTER_FIELDS
from workroomsapp.models import Lecturer, Customer

__all__ = [
    'HumanFilter',
    'LecturerFilter',
    'CustomerFilter'
]


class HumanFilter(BaseFilter):
    """
    Класс для фильтрации сторон взаимодействия на сервисе (Лектор, Заказчик...).

    При наследовании:
    exclude: list[FilterField] - какие объекты исключить из фильтрации.

    """

    # этот метод можно будет убрать, когда будем менять базу
    def _build_exclude_dict(self) -> dict:
        """ Выстраивает словарь, в котором ключ - путь, используя ORM, к пользователю от текущей модели.
        А значение - сам пользователь """
        
        query_string = 'person__user'
        return {query_string: self.from_obj}
    
    def _default_filter_queryset(self):
        qs = super()._default_filter_queryset()
        exclude = self._build_exclude_dict()
        return qs.exclude(**exclude)


class LecturerFilter(HumanFilter):
    model = Lecturer
    fields = LECTURER_FILTER_FIELDS


class CustomerFilter(HumanFilter):
    model = Customer
    fields = CUSTOMER_FILTER_FIELDS
