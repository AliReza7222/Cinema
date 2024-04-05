from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache

from .models import UserSite
from TheCinema import response_msg as msg


class CompleteCheckInfoUserPermission(BasePermission):
    message = msg.ERROR_PERMISSION_STEP_TWO_SIGNIN

    def has_permission(self, request, view):
        try:
            user = UserSite.objects.get(user_uuid=view.kwargs.get('user_uuid'))
            if not cache.has_key(user.password):
                return False
            return True
        except UserSite.DoesNotExist:
            return False
