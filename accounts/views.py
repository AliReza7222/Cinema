from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView

from .models import UserSite
from TheCinema import response_msg as msg
from .utils import (
    get_toke,
    send_sms_token_login,
    create_password,
    authentication_user)
from .serializrs import (
    SignUpSerializer,
    SignInStepOneSerializer,
    SignInStepTwoSerializer,
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


class StepOneSignInView(GenericAPIView):
    """ step one : check phone number and password valid. """
    serializer_class = SignInStepOneSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data.get("phone_number")
            password = serializer.validated_data.get("password")
            user = authentication_user(phone_number, password)
            if user:
                token = str(get_toke())
                message_token = msg.SEND_TOKEN_TO_USER.format(token=token)
                response = send_sms_token_login(phone_number, message_token)
                if response == 200:
                    cache.set(user.password, token, timeout=70)
                    return Response(
                        {
                            'message': msg.SUCCESS_SEND_SMS,
                            'type': 'success',
                            'data': {'user-phone-number': phone_number}
                        },
                        status=status.HTTP_200_OK)
                elif response == 408:
                    return Response(
                        {'message': msg.ERROR_SEND_SMS, 'type': 'error'}, status=status.HTTP_408_REQUEST_TIMEOUT)
            return Response(
                {'message': msg.ERROR_AUTHENTICATION_USER, 'type': 'error'}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {'message': serializer.errors, 'type': 'error'}, status=status.HTTP_400_BAD_REQUEST)


# class SignInView(APIView):
#
#     def send_sms_to_user(self, phone_number):
#         message = 'کد به شماره تلفن کاربر ارسال شد .'
#         token = str(get_toke())
#         message_send = f'کد ورود شما به سایت {token} است .'
#         send_obj = send_sms_token_login(phone_number, message_send)
#         cache.set(f"{phone_number}_user", token, timeout=70)
#         # print token for develop project
#         print(token)
#         return message
#
#     def post(self, request, *args, **kwargs):
#         if kwargs.get('step') == '1':
#             serializer = SignInStepOneSerializer(data=request.data)
#             if serializer.is_valid():
#                 data = serializer.validated_data
#                 phone_number, password = data.get('phone_number'), data.get('password')
#                 valid_info = self.check_user(phone_number, password)
#                 if valid_info:
#                     result = self.send_sms_to_user(phone_number)
#                     user = valid_info
#                     response = Response({'message': result, 'step_now': 'Ok', 'step_continue': '2',
#                                          'user': user.id},
#                                         status=status.HTTP_200_OK)
#                     return response
#             return Response({'message': 'phone number or password invalid !'}, status=status.HTTP_404_NOT_FOUND)
#
#         elif kwargs.get('step') == '2':
#             id_user = request.GET.get('user')
#             user = UserSite.objects.get(id=id_user)
#             phone_number = user.phone_number
#             serializer = SignInStepTwoSerializer(data=request.data)
#             real_token = cache.get(f"{phone_number}_user")
#             if serializer.is_valid():
#                 data = serializer.validated_data
#                 if real_token and (data.get('verification_code') == real_token):
#                     # Create a Token Jwt for login User
#                     user = UserSite.objects.get(phone_number=phone_number)
#                     refresh_token = RefreshToken.for_user(user=user)
#                     access_token = refresh_token.access_token
#                     return Response({'refresh_token': str(refresh_token), 'access_token': str(access_token)},
#                                     status=status.HTTP_200_OK)
#
#             return Response({'message': 'code is invalid !'}, status=status.HTTP_404_NOT_FOUND)


class ChangePasswordView(APIView):

    def send_message_to_user(self, message, phone_number):
        send_sms_token_login(phone_number, message)

    def post(self, request, *args, **kwargs):
        data = request.data
        step = kwargs.get('step')

        if step == '1':
            serializer = GetPhoneNumberSerializer(data=data)
            if serializer.is_valid():
                phone_number = serializer.validated_data.get('phone_number')
                try:
                    user = UserSite.objects.get(phone_number=phone_number)
                    phone_number = user.phone_number
                    token = str(get_toke())
                    message = f'کد تایید شماره شما بعنوان یک کاربر این سایت {token}'
                    cache.set(phone_number, token, timeout=70)
                    self.send_message_to_user(message, phone_number)
                    # print message code for develop project
                    print(message, '------', token)
                    return Response({'message': 'code verification send to user .', 'step_one': 'ok',
                                     'step_continue': '2', 'phone_number': str(user.phone_number)}
                                    , status=status.HTTP_200_OK)

                except ObjectDoesNotExist:
                    return Response({'message': 'Phone Number Invalid !'}, status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif step == '2':
            serializer = SignInStepTwoSerializer(data=data)
            if serializer.is_valid():
                phone_number = request.GET.get('phone_number')
                user = UserSite.objects.get(phone_number=phone_number)
                code = serializer.validated_data.get('verification_code')
                token = cache.get(phone_number)
                if token and (token == code):
                    new_password = create_password()
                    user.set_password(new_password)
                    message = f"رمز عبور جدید شما {new_password} است  ."
                    self.send_message_to_user(message, phone_number)
                    user.save()
                    # print message for develop project
                    print(message)
                    return Response({'message': 'Successfully changed password , new password send your phone number '},
                                    status=status.HTTP_200_OK)

            return Response({'error': 'code is invalid !'}, status=status.HTTP_400_BAD_REQUEST)
