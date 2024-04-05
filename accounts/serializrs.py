import re

from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import UserSite
from TheCinema import response_msg as msg


class SignUpSerializer(serializers.ModelSerializer):

    re_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserSite
        fields = [
            'phone_number',
            'password',
            're_password'
        ]

    def validate_phone_number(self, value):
        check_phone_number = re.findall('^09[0-9]{9}$', value) or None
        if check_phone_number is None:
            raise serializers.ValidationError(msg.ERROR_INVALID_PHONE_NUMBER)
        return value

    def validate_password(self, value):
            if len(value) < 6:
                raise serializers.ValidationError(msg.ERROR_INVALID_PASSWORD)
            return value

    def validate(self, data):
        password, confirm = data.get('password'), data.get('re_password')
        if password != confirm:
            raise serializers.ValidationError({'password':msg.ERROR_INVALID_RE_PASSWORD})
        return data

    def create(self, validated_data):
        del validated_data['re_password']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class CheckInformationUserSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)


class CheckTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=6, write_only=True)


class GetPhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
