from django.core.cache import cache
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView

from .utils import get_toke, send_sms_token_login
from .models import UserSite
from .serializrs import SignUpSerializer, SignInStepOneSerializer, SignInStepTwoSerializer


class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializer


class SignInView(APIView):

    def check_user(self, phone_number, password):
        find_user = UserSite.objects.filter(phone_number=phone_number)
        if find_user:
            user = find_user[0]
            check_password_user = check_password(password, user.password)
            if check_password_user:
                return True
        return False

    def send_sms_to_user(self, phone_number):
        message = 'کد به شماره تلفن کاربر ارسال شد .'
        token = str(get_toke())
        send_obj = send_sms_token_login(token, phone_number)
        cache.set(f"{phone_number}_user", token, timeout=70)
        # print token for develop project
        print(token)
        return message

    def post(self, request, *args, **kwargs):
        step = request.GET.get('step')
        if step == '1':
            serializer = SignInStepOneSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                phone_number, password = data.get('phone_number'), data.get('password')
                valid_info = self.check_user(phone_number, password)
                if valid_info:
                    result = self.send_sms_to_user(phone_number)

                    response = Response({'message': result, 'step_now': 'Ok', 'step_continue': '2'},
                                        status=status.HTTP_200_OK)
                    return response
            return Response({'message': 'phone number or password invalid !'}, status=status.HTTP_404_NOT_FOUND)

        elif step == '2':
            phone_number = request.GET.get('phone_number')
            serializer = SignInStepTwoSerializer(data=request.data)
            real_token = cache.get(f"{phone_number}_user")
            if serializer.is_valid():
                data = serializer.validated_data
                if real_token and (data.get('verification_code') == real_token):
                    # Create a Token Jwt for login User
                    user = UserSite.objects.get(phone_number=phone_number)
                    refresh_token = RefreshToken.for_user(user=user)
                    access_token = refresh_token.access_token
                    return Response({'refresh_token': str(refresh_token), 'access_token': str(access_token)},
                                    status=status.HTTP_200_OK)

            return Response({"message": 'code is invalid !'}, status=status.HTTP_404_NOT_FOUND)


class RefreshTokenView(APIView):

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response({'error': 'Please provide a refresh token.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token
            return Response({'access_token': str(access_token)}, status=status.HTTP_200_OK)

        except TokenError:
            return Response({'error': 'Invalid refresh token.'}, status=status.HTTP_401_UNAUTHORIZED)