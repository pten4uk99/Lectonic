from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

from workroomsapp.models import Person

User = get_user_model()


class IsLecturer(BasePermission):
    """ Предоставляет доступ только лекторам. """

    def has_permission(self, request, view):
        return (isinstance(request.user, User) and
                Person.objects.filter(user=request.user).first() and
                request.user.person.is_lecturer)


class IsProjectAdmin(BasePermission):
    """ Предоставляет доступ только админитраторам проекта. """

    def has_permission(self, request, view):
        return (isinstance(request.user, User) and
                Person.objects.filter(user=request.user).first() and
                request.user.person.is_project_admin)


class IsCustomer(BasePermission):
    """ Предоставляет доступ только заказчикам. """

    def has_permission(self, request, view):
        return (isinstance(request.user, User) and
                Person.objects.filter(user=request.user).first() and
                request.user.person.is_customer)


class IsVerified(BasePermission):
    """ Предоставляет доступ только пользователям, у которых документы
    проверены модераторами. """

    def has_permission(self, request, view):
        return (isinstance(request.user, User) and
                Person.objects.filter(user=request.user).first() and
                request.user.person.is_verified)
