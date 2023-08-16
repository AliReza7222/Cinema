from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import UserSite


class SignUpSerializers(serializers.ModelSerializer):

    re_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserSite
        fields = [
            'username',
            'email',
            'password',
            're_password'
        ]

    def validate_password(self, value):
            if len(value) < 6:
                raise serializers.ValidationError("Password must be 6 characters longer !")
            return value

    def validate(self, data):
        password, confirm = data.get('password'), data.get('re_password')
        if password != confirm:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        del validated_data['re_password']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
