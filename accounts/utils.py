import random, uuid
from string import ascii_uppercase, ascii_lowercase, digits
from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.core.cache import cache
from kavenegar import *

from .models import UserSite


def authentication_user(phone_number: str, password: str):
    find_user = UserSite.objects.filter(phone_number=phone_number)
    if find_user.exists():
        user = find_user.first()
        if check_password(password, user.password):
            return user
    return None


def get_toke() -> int:
    return random.randint(100000, 999999)


def create_password() -> str:
    words = list(ascii_uppercase + ascii_lowercase + digits)
    password = ''.join(random.choices(words, k=16))
    return password


def send_sms_token_login(phone_number, message):
    try:
        api = KavenegarAPI(settings.APIKEY)
        params = {
            'sender': settings.PHONE_NUMBER,
            'receptor': phone_number,
            'message': message
        }
        # use code under for send code to users when buy a service from Kavenegar
        # ** in develop so i comment codes send token to user .
        # info = api.sms_send(params)
        # response = info.get('return')
        # return response.status
        # for dev
        return 200  # sucess status
    except APIException:
        return 408  # timeout status : error 408
    except HTTPException:
        return 408  # timeout status : error 408


def get_key_permission(permission: str, user: UserSite):
    if permission == 'signin':
        key = user.password
    elif permission == 'forget_password':
        key = f"{user.password}_fpass"
    return key


def check_key_cache(permission: str, user_uuid: uuid.UUID):
    user = UserSite.objects.filter(user_uuid=user_uuid)
    if user.exists():
        key = get_key_permission(permission=permission, user=user.first())
        if cache.has_key(key):
            return True
    return False
