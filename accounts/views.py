from django.core.cache import cache
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import PermissionDenied, NotAuthenticated

from TheCinema import response_msg as msg
from utils import auth_user, send_token, valid_operation_url
from . import permissions, serializers
from .models import UserSite


class GetPhoneNumberView(GenericAPIView):
    """
        step one : check phone number for register or login or forget password
        so send token to your phone number .
    """
    serializer_class = serializers.GetPhoneNumberSerializer

    def response_send_token(self, phone_number):
        token = str(auth_user.get_toke())
        message_token = msg.SEND_TOKEN_TO_USER.format(token=token)
        response = send_token.send_sms_token(phone_number, message_token)
        if response == status.HTTP_200_OK:
            cache.set(phone_number, token, timeout=70)  # set token with key phone number in cache
            return Response(
                {
                    'message': msg.SUCCESS_SEND_SMS, 'type': 'success', 'data': {'phone_number': phone_number},
                    'token': f"We are developing the project, so our token is {token}"
                },
                status=status.HTTP_200_OK)
        elif response == status.HTTP_408_REQUEST_TIMEOUT:
            return Response(
                {'message': msg.ERROR_SEND_SMS, 'type': 'error'},
                status=status.HTTP_408_REQUEST_TIMEOUT)

    def post(self, request, *args, **kwargs):
        operation = kwargs.get('op')
        if response_check_operation := valid_operation_url.invalid_operation(op=operation):
            return Response(response_check_operation, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data.get('phone_number')
            # check operatin in (forget_password, register, login)
            if response_check_op := valid_operation_url.check_operation_view(operation, phone_number):
                return Response(response_check_op, status=status.HTTP_404_NOT_FOUND)
            cache.set('permission_step_two', operation, timeout=70)  # set operation with key permission_step_two in cache
            return self.response_send_token(phone_number)  # response send my token to user's phone number
        return Response(
            {'message': serializer.errors, 'type': 'error'},
            status=status.HTTP_400_BAD_REQUEST)


class CheckTokenView(GenericAPIView):
    """ step two : check token so doing login or register or forget password  """
    permission_classes = (permissions.CheckStepForm, permissions.CheckExistsToken)
    serializer_class = serializers.CheckTokenSerializer

    def permission_denied(self, request, message=None, code=None):
        raise PermissionDenied(message)

    def response_login_user(self, phone_number):
        return Response(
            {'message': msg.SUCESS_LOGIN, 'type': 'success',
             'data': auth_user.login_user(phone_number=phone_number)},
            status=status.HTTP_200_OK)

    def response_register_user(self, phone_number):
        UserSite.objects.create(phone_number=phone_number)
        return Response(
            {'message': msg.SUCCESS_REGISTER, 'type': 'success'},
            status=status.HTTP_200_OK
        )

    def response_forget_password(self, phone_number):
        new_password = auth_user.create_password()
        user = get_object_or_404(UserSite, phone_number=phone_number)
        user.set_password(new_password)
        user.save()
        return Response(
            {'message': msg.SUCESS_SET_FORGET_PASSWORD.format(new_password=new_password), 'type': 'success'},
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        operation, phone_number = kwargs.get('op'), kwargs.get('phone_number')
        if response_check_operation := valid_operation_url.invalid_operation(op=operation):
            return Response(response_check_operation, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data.get('token')
            if token == cache.get(kwargs.get('phone_number')):
                permission_step_two = cache.get('permission_step_two')
                if operation != permission_step_two:  # check same operation and permission_step_two in cache
                    return Response(
                        {'message': msg.ERROR_INVALID_URL, 'type': 'error'},
                        status=status.HTTP_404_NOT_FOUND)
                elif permission_step_two == 'login':
                    return self.response_login_user(phone_number=phone_number)
                elif permission_step_two == 'register':
                    return self.response_register_user(phone_number=phone_number)
                elif permission_step_two == 'forget_password':
                    return self.response_forget_password(phone_number=phone_number)
            return Response(
                {'message': msg.ERROR_INVALID_TOKEN_LOGIN, 'type': 'error'},
                status.HTTP_404_NOT_FOUND)
        return Response(
            {'message': serializer.errors, 'type': 'error'},
            status=status.HTTP_400_BAD_REQUEST
        )


class CompleteAuthentication(GenericAPIView):
    """ now complete authentication is just set password for user ."""
    permission_classes = (IsAuthenticated, permissions.CheckPassword)
    serializer_class = serializers.AuthenticationCompleteSerializer

    def permission_denied(self, request, message=None, code=None):
        if request.authenticators and not request.successful_authenticator:
            raise NotAuthenticated()
        raise PermissionDenied(detail=message, code=code)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data.get('password'))
            user.save()
            return Response(
                {'message': msg.SUCESS_SET_PASSWORD, 'type': 'success'},
                status=status.HTTP_200_OK)
        return Response(
            {'message': serializer.errors, 'type': 'error'},
            status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('password')
            user = request.user
            if not check_password(old_password, user.password):
                return Response(
                    {'message': msg.ERROR_OLD_PASSWORD_INVALID, 'type': 'error'},
                    status=status.HTTP_404_NOT_FOUND)
            user.set_password(new_password)
            user.save()
            return Response(
                {'message': msg.SUCCESS_CHANGE_PASSWORD, 'type': 'success'}, status=status.HTTP_200_OK)
        return Response({'message': serializer.errors, 'type': 'error'}, status=status.HTTP_400_BAD_REQUEST)


class CompleteProfileView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.CompleteProfileSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user.profileuser, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': msg.SUCESS_COMPLETE_PROFILE, 'type': 'sucess', 'data': serializer.data},
                status=status.HTTP_200_OK)
        return Response(
            {'message': serializer.errors, 'type': 'error'}, status=status.HTTP_400_BAD_REQUEST
        )


class LoginWithPasswordView(GenericAPIView):
    serializer_class = serializers.LoginWithPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data.get('phone_number')
            password = serializer.validated_data.get('password')
            user = auth_user.authentication_user(phone_number, password)
            if user:
                return Response(
                    {'message': msg.SUCESS_LOGIN, 'type': 'success', 'data': auth_user.login_user(user=user)},
                    status=status.HTTP_200_OK)
            return Response(
                {'message': msg.ERROR_LOGIN_USER, 'type': 'error'},
                status=status.HTTP_404_NOT_FOUND)
        return Response(
            {'message': serializer.errors, 'type': 'error'},
            status=status.HTTP_400_BAD_REQUEST)
