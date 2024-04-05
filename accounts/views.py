from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.exceptions import PermissionDenied

from .models import UserSite
from .permissions import CompleteCheckInfoUserPermission
from TheCinema import response_msg as msg
from .utils import (
    get_toke,
    send_sms_token_login,
    create_password,
    authentication_user)
from .serializrs import (
    SignUpSerializer,
    CheckInformationUserSerializer,
    CheckTokenSerializer,
    GetPhoneNumberSerializer
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
            user = authentication_user(phone_number, password)
            if user:
                token = str(get_toke())
                print(token) # for devlope and test
                message_token = msg.SEND_TOKEN_TO_USER.format(token=token)
                response = send_sms_token_login(phone_number, message_token)
                if response == status.HTTP_200_OK:
                    cache.set(user.password, token, timeout=70)
                    return Response(
                        {
                            'message': msg.SUCCESS_SEND_SMS,
                            'type': 'success',
                            'data': {'user': str(user.user_uuid)}
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
    permission_classes = (CompleteCheckInfoUserPermission, )
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



# class ChangePasswordView(APIView):
#
#     def send_message_to_user(self, message, phone_number):
#         send_sms_token_login(phone_number, message)
#
#     def post(self, request, *args, **kwargs):
#         data = request.data
#         step = kwargs.get('step')
#
#         if step == '1':
#             serializer = GetPhoneNumberSerializer(data=data)
#             if serializer.is_valid():
#                 phone_number = serializer.validated_data.get('phone_number')
#                 try:
#                     user = UserSite.objects.get(phone_number=phone_number)
#                     phone_number = user.phone_number
#                     token = str(get_toke())
#                     message = f'کد تایید شماره شما بعنوان یک کاربر این سایت {token}'
#                     cache.set(phone_number, token, timeout=70)
#                     self.send_message_to_user(message, phone_number)
#                     # print message code for develop project
#                     print(message, '------', token)
#                     return Response({'message': 'code verification send to user .', 'step_one': 'ok',
#                                      'step_continue': '2', 'phone_number': str(user.phone_number)}
#                                     , status=status.HTTP_200_OK)
#
#                 except ObjectDoesNotExist:
#                     return Response({'message': 'Phone Number Invalid !'}, status=status.HTTP_404_NOT_FOUND)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         elif step == '2':
#             serializer = SignInStepTwoSerializer(data=data)
#             if serializer.is_valid():
#                 phone_number = request.GET.get('phone_number')
#                 user = UserSite.objects.get(phone_number=phone_number)
#                 code = serializer.validated_data.get('verification_code')
#                 token = cache.get(phone_number)
#                 if token and (token == code):
#                     new_password = create_password()
#                     user.set_password(new_password)
#                     message = f"رمز عبور جدید شما {new_password} است  ."
#                     self.send_message_to_user(message, phone_number)
#                     user.save()
#                     # print message for develop project
#                     print(message)
#                     return Response({'message': 'Successfully changed password , new password send your phone number '},
#                                     status=status.HTTP_200_OK)
#
#             return Response({'error': 'code is invalid !'}, status=status.HTTP_400_BAD_REQUEST)
