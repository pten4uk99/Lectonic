from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission
from rest_framework import exceptions

User = get_user_model()

class GotProfile(BasePermission):
    """ Проверка имеется ли профиль у юзера """
    message = 'У пользователя не добавлен профиль'

    def has_permission(self, request, view):
        try:
            return request.user.person.get(id = request.user.pk).exist()
        except:
            raise exceptions.PermissionDenied(detail=self.message)

class IsLecturer(BasePermission):
    """ Предоставляет доступ только лекторам. """
    message1 = 'У пользователя не добавлен профиль'
    message2 = 'Пользователь не лектор'
    def has_permission(self, request, view):
        try:
            has_profile = request.user.person.is_lecturer
        except:
            raise exceptions.PermissionDenied(detail=self.message1)
        if (isinstance(request.user, User) and has_profile):
            return True
        else:
            raise exceptions.PermissionDenied(detail=self.message2)


class IsProjectAdmin(BasePermission):
    """ Предоставляет доступ только админитраторам проекта. """

    def has_permission(self, request, view):
        return isinstance(request.user, User) and request.user.person.is_project_admin


class IsCustomer(BasePermission):
    """ Предоставляет доступ только заказчикам. """

    def has_permission(self, request, view):
        return isinstance(request.user, User) and request.user.person.is_customer


class IsVerified(BasePermission):
    """ Предоставляет доступ только пользователям, у которых документы
    проверены модераторами. """

    def has_permission(self, request, view):
        return isinstance(request.user, User) and request.user.person.is_verified