import random
from kavenegar import *
from django.conf import settings


def get_toke():
    return random.randint(100000, 999999)


def send_sms_token_login(token, phone_number):
    apikey = settings.APIKEY
    sender = settings.PHONE_NUMBER
    api = KavenegarAPI(apikey)
    params = {
        'sender': sender,
        'receptor': phone_number,
        'message': f'این یک تست برای ورود است کد ورود شما {token} '
    }
    # use code under for send code to users when buy a service from Kavenegar
    # -----> response = api.sms_send(params)
    response = api.sms_send(params)
    # response = params['message']
    return response

