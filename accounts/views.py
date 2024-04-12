from django.core.cache import cache
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.exceptions import PermissionDenied, NotAuthenticated

from . import utils, permissions
from .models import UserSite, ProfileUser
from TheCinema import response_msg as msg
from .serializrs import (
    AuthenticationCompleteSerializer,
    CheckTokenSerializer,
    GetPhoneNumberSerializer,
    ChangePasswordSerializer,
    CompleteProfileSerializer,
    LoginWithPassword
)


class GetPhoneNumberView(GenericAPIView):
    """
        step one : check phone number for register or login or forget passwrod
        so send token to your phone number .
    """
    serializer_class = GetPhoneNumberSerializer

    def post(self, request, *args, **kwargs):
        operations = ('register', 'login', 'forget_password')
        if kwargs.get('op') not in operations:
            return Response(
                {'message': msg.ERROR_INVALID_URL, 'type': 'error'},
                status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data.get('phone_number')
            find_number = UserSite.objects.filter(phone_number=phone_number)
            if kwargs.get('op') == operations[0] and find_number.exists():
                return Response(
                    {'message': msg.ERROR_DUPLICATE_PHONE_NUMBER, 'type': 'error'},
                    status=status.HTTP_400_BAD_REQUEST)
            elif kwargs.get('op') in operations[1:] and not find_number.exists():
                return Response(
                    {'message': msg.ERROR_NOT_EXISTS_PHONE_NUMBER, 'type': 'error'},
                    status=status.HTTP_400_BAD_REQUEST)
            else:
                token = str(utils.get_toke())
                message_token = msg.SEND_TOKEN_TO_USER.format(token=token)
                response = utils.send_sms_token_login(phone_number, message_token)
                if response == status.HTTP_200_OK:
                    cache.set(phone_number, token, timeout=70)
                    return Response(
                        {
                            'message': msg.SUCCESS_SEND_SMS,
                            'type': 'success',
                            'data': {'phone_number': phone_number},
                            'token': f"We are developing the project, so our token is {token}"
                        },
                        status=status.HTTP_200_OK)
                elif response == status.HTTP_408_REQUEST_TIMEOUT:
                    return Response(
                        {'message': msg.ERROR_SEND_SMS, 'type': 'error'},
                        status=status.HTTP_408_REQUEST_TIMEOUT)
        return Response(
            {'message': serializer.errors, 'type': 'error'},
            status=status.HTTP_400_BAD_REQUEST)


class CheckTokenView(GenericAPIView):
    """ step two : check token so doing login or register or forget password  """
    permission_classes = (permissions.CheckExistsToken, )
    serializer_class = CheckTokenSerializer

    def permission_denied(self, request, message=None, code=None):
        raise PermissionDenied(message)

    def post(self, request, *args, **kwargs):
        operations = ('register', 'login', 'forget_password')
        if kwargs.get('op') not in operations:
            return Response(
                {'message': msg.ERROR_INVALID_URL, 'type': 'error'},
                status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data.get('token')
            if token == cache.get(kwargs.get('phone_number')):
                if kwargs.get('op') == operations[1]:
                    return Response(
                        {'message': msg.SUCESS_LOGIN,
                        'type': 'sucess',
                        'data': utils.login_user(phone_number=kwargs.get('phone_number'))},
                        status=status.HTTP_200_OK)
                elif kwargs.get('op') == operations[0]:
                    UserSite.objects.create(phone_number=kwargs.get('phone_number'))
                    return Response(
                        {'message': msg.SUCCESS_REGISTER, 'type': 'sucess'},
                        status=status.HTTP_200_OK
                    )
                elif kwargs.get('op') == operations[2]:
                    new_password = utils.create_password()
                    user = get_object_or_404(UserSite, phone_number=kwargs.get('phone_number'))
                    user.set_password(new_password)
                    user.save()
                    return Response(
                        {'message': msg.SUCESS_SET_FORGET_PASSWORD.format(new_password=new_password),
                        'type': 'success'},
                        status=status.HTTP_200_OK
                    )
            return Response(
                {'message': msg.ERROR_INVALID_TOKEN_LOGIN, 'type': 'error'},
                status.HTTP_404_NOT_FOUND)
        return Response(
            {'message': serializer.errors, 'type': 'error'},
            status=status.HTTP_400_BAD_REQUEST
        )


class CompleteAuthentication(GenericAPIView):
    permission_classes = (IsAuthenticated, permissions.CheckPassword)
    serializer_class = AuthenticationCompleteSerializer

    def permission_denied(self, request, message=None, code=None):
        if request.authenticators and not request.successful_authenticator:
            raise NotAuthenticated()
        raise PermissionDenied(detail=message, code=code)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data.get('password'))
            request.user.save()
            return Response(
                {'message': msg.SUCESS_SET_PASSWORD, 'type': 'sucess'},
                status=status.HTTP_200_OK)
        return Response(
            {'message': serializer.errors, 'type': 'error'},
            status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')
            if not check_password(old_password, request.user.password):
                return Response(
                    {'message': msg.ERROR_OLD_PASSWORD_INVALID, 'type': 'error'},
                    status=status.HTTP_404_NOT_FOUND)
            request.user.set_password(new_password)
            request.user.save()
            return Response(
                {'message': msg.SUCCESS_CHANGE_PASSWORD, 'type': 'sucess'}, status=status.HTTP_200_OK)
        return Response({'message': serializer.errors, 'type': 'error'}, status=status.HTTP_400_BAD_REQUEST)


class CompleteProfileView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CompleteProfileSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            ProfileUser.objects.filter(user=request.user).update(**serializer.validated_data)
            return Response(
                {'message': msg.SUCESS_COMPLETE_PROFILE, 'type': 'sucess'},
                status = status.HTTP_200_OK)
        return Response(
            {'message': serializer.errors, 'type': 'error'}, status=status.HTTP_400_BAD_REQUEST
        )


class LoginWithPassword(GenericAPIView):
    serializer_class = LoginWithPassword

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone_number = kwargs.get('phone_number')
            password = serializer.validated_data.get('password')
            user = utils.authentication_user(phone_number, password)
            if user:
                return Response(
                    {'message': msg.SUCESS_LOGIN,
                    'type': 'sucess',
                    'data': utils.login_user(user=user)},
                    status=status.HTTP_200_OK)
            return Response(
                {'message': msg.ERROR_LOGIN_USER, 'type': 'error'},
                status=status.HTTP_404_NOT_FOUND)
        return Response(
            {'message': serializer.errors, 'type': 'error'},
            status=status.HTTP_400_BAD_REQUEST)
