import random
from string import ascii_uppercase, ascii_lowercase, digits
from kavenegar import *
from django.conf import settings


def get_toke():
    return random.randint(100000, 999999)


def create_password():
    words = list(ascii_uppercase + ascii_lowercase + digits)
    password = ''.join(random.choices(words, k=6))
    return password


def send_sms_token_login(phone_number, message):
    apikey = settings.APIKEY
    sender = settings.PHONE_NUMBER
    api = KavenegarAPI(apikey)
    params = {
        'sender': sender,
        'receptor': phone_number,
        'message': message
    }
    # use code under for send code to users when buy a service from Kavenegar
    # -----> response = api.sms_send(params)
    # response = api.sms_send(params)
    # Now is in develop project so response is a str equal send ok
    response = 'send ok'
    return response

