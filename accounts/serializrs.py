import re

from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import UserSite, ProfileUser
from TheCinema import response_msg as msg


class BaseSetPasswordUserSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)

    def validate_password(self, value):
            if len(value) < 8:
                raise serializers.ValidationError(msg.ERROR_INVALID_PASSWORD)
            return value

    def validate(self, data):
        password = data.get('password')
        re_password = data.get('re_password')
        if not password == re_password:
            raise serializers.ValidationError({'password': msg.ERROR_INVALID_RE_PASSWORD})
        return data


class AuthenticationCompleteSerializer(BaseSetPasswordUserSerializer):
    pass


class CheckTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=6, write_only=True)


class GetPhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate_phone_number(self, value):
        check_phone_number = re.findall('^09[0-9]{9}$', value) or None
        if check_phone_number is None:
            raise serializers.ValidationError(msg.ERROR_INVALID_PHONE_NUMBER)
        return value


class ChangePasswordSerializer(BaseSetPasswordUserSerializer):
    old_password = serializers.CharField(write_only=True)


class CompleteProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileUser
        fields = [
            'first_name',
            'last_name',
            'photo'
        ]


class LoginWithPassword(serializers.Serializer):
    password = serializers.CharField(write_only=True)
