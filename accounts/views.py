from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.exceptions import PermissionDenied

from . import utils, permissions
from .models import UserSite
from TheCinema import response_msg as msg
from .serializrs import (
    SignUpSerializer,
    CheckInformationUserSerializer,
    CheckTokenSerializer,
    GetPhoneNumberSerializer,
    ChangePasswordSerializer
)


class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {'type': 'success', 'message': msg.SUCCESS_REGISTER, 'data': serializer.data},
            status=status.HTTP_201_CREATED,
        )


class CheckInformationUserView(GenericAPIView):
    """ step one signin user: check phone number and password valid. """
    serializer_class = CheckInformationUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data.get("phone_number")
            password = serializer.validated_data.get("password")
            user = utils.authentication_user(phone_number, password)
            if user:
                token = str(utils.get_toke())
                message_token = msg.SEND_TOKEN_TO_USER.format(token=token)
                response = utils.send_sms_token_login(phone_number, message_token)
                if response == status.HTTP_200_OK:
                    cache.set(user.password, token, timeout=70)
                    return Response(
                        {
                            'message': msg.SUCCESS_SEND_SMS,
                            'type': 'success',
                            'data': {'user': str(user.user_uuid)},
                            'token': f"We are developing the project, so our token is {token}"
                        },
                        status=status.HTTP_200_OK)
                elif response == status.HTTP_408_REQUEST_TIMEOUT:
                    return Response(
                        {'message': msg.ERROR_SEND_SMS, 'type': 'error'}, status=status.HTTP_408_REQUEST_TIMEOUT)
            return Response(
                {'message': msg.ERROR_AUTHENTICATION_USER, 'type': 'error'}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {'message': serializer.errors, 'type': 'error'}, status=status.HTTP_400_BAD_REQUEST)


class CheckTokenView(GenericAPIView):
    """ step two signin user: checks the token sent to your phone number  """
    permission_classes = (permissions.CompleteCheckInfoUserSignIn, )
    serializer_class = CheckTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(UserSite, user_uuid=kwargs.get('user_uuid'))
            token = serializer.validated_data.get('token')
            if token == cache.get(user.password):
                refresh = RefreshToken.for_user(user)
                return Response(
                    {'tokens': {'refresh': str(refresh),'access': str(refresh.access_token)},
                    'message': msg.SUCESS_SIGNIN,
                    'type': 'success'},
                    status=status.HTTP_200_OK
                )
            return Response({'message': msg.INVALID_TOKEN_LOGIN, 'type': 'error'}, status.HTTP_404_NOT_FOUND)
        return Response(
            {'message': serializer.errors, 'type': 'error'}, status=status.HTTP_400_BAD_REQUEST
        )

    def permission_denied(self, request, message=None, code=None):
        raise PermissionDenied(message)


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


class SendTokenForgetPasswordView(GenericAPIView):
    """ step one forget password: send a token forget password to user's phone number """
    serializer_class = GetPhoneNumberSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data.get("phone_number")
            user = UserSite.objects.filter(phone_number=phone_number)
            if user.exists():
                token_forget_password = str(utils.get_toke())
                response = utils.send_sms_token_login(phone_number, token_forget_password)
                if response == status.HTTP_200_OK:
                    cache.set(f"{user.first().password}_fpass", token_forget_password, timeout=70)
                    return Response(
                        {
                            'message': msg.SUCCESS_SEND_TOKEN_FORGET_PASSWORD,
                            'type': 'success',
                            'data': {'user_uuid': str(user.first().user_uuid)},
                            'token': f"We are developing the project, so our token is {token_forget_password}"
                        },
                        status=status.HTTP_200_OK)
                elif response == status.HTTP_408_REQUEST_TIMEOUT:
                    return Response(
                        {'message': msg.ERROR_SEND_SMS, 'type': 'error'}, status=status.HTTP_408_REQUEST_TIMEOUT)
            return Response(
                {'message': msg.ERROR_AUTHENTICATION_USER, 'type': 'error'}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {'message': serializer.errors, 'type': 'error'}, status=status.HTTP_400_BAD_REQUEST)


class GetForgetPasswordView(GenericAPIView):
    """ step two forget password : check valid token forget password and set a new password """
    permission_classes = (permissions.CompleteCheckUserForgetPassword, )
    serializer_class = CheckTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(UserSite, user_uuid=kwargs.get('user_uuid'))
            token = serializer.validated_data.get('token')
            if token == cache.get(f"{user.password}_fpass"):
                new_password = utils.create_password()
                user.set_password(new_password)
                user.save()
                return Response(
                    {'message': msg.SUCESS_SET_FORGET_PASSWORD.format(new_password=new_password),
                    'type': 'success'},
                    status=status.HTTP_200_OK
                )
            return Response({'message': msg.INVALID_TOKEN_LOGIN, 'type': 'error'}, status.HTTP_404_NOT_FOUND)
        return Response(
            {'message': serializer.errors, 'type': 'error'}, status=status.HTTP_400_BAD_REQUEST
        )

    def permission_denied(self, request, message=None, code=None):
        raise PermissionDenied(message)
