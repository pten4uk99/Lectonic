from rest_framework.permissions import BasePermission


class IsLecturer(BasePermission):
    """ Предоставляет доступ только лекторам. """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_lecturer)


class IsProjectAdmin(BasePermission):
    """ Предоставляет доступ только админитраторам проекта. """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_project_admin)


class IsCustomer(BasePermission):
    """ Предоставляет доступ только заказчикам. """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_customer)


class IsVerified(BasePermission):
    """ Предоставляет доступ только пользователям, у которых документы
    проверены модераторами. """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_verified)
