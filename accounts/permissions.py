from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import status

from .models import UserSite
from .utils import check_key_cache
from TheCinema import response_msg as msg


class CompleteCheckInfoUserSignIn(BasePermission):
    message = msg.ERROR_PERMISSION_STEP_TWO

    def has_permission(self, request, view):
        return check_key_cache(permission='signin', user_uuid=view.kwargs.get('user_uuid'))


class CompleteCheckUserForgetPassword(BasePermission):
    message = msg.ERROR_PERMISSION_STEP_TWO

    def has_permission(self, request, view):
        return check_key_cache(permission='forget_password', user_uuid=view.kwargs.get('user_uuid'))
