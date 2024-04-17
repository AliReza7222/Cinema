from rest_framework.permissions import BasePermission
from rest_framework import status
from django.core.cache import cache


from .models import UserSite
from TheCinema import response_msg as msg


class CheckStepForm(BasePermission):
    message = msg.ERROR_EXISTS_TOKEN_OR_STEP_FORM

    def has_permission(self, request, view):
        permission_next_step = cache.get('permission_step_two')
        if permission_next_step:
            print(permission_next_step, type(permission_next_step))
            return True
        return False


class CheckExistsToken(BasePermission):
    message = msg.ERROR_EXISTS_TOKEN_OR_STEP_FORM

    def has_permission(self, request, view):
        return cache.has_key(view.kwargs.get('phone_number'))


class CheckPassword(BasePermission):
    message = msg.ERROR_SET_PASSWORD_FOR_FIRST

    def has_permission(self, request, view):
        if request.user.password:
            return False
        return True
