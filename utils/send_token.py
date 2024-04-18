from django.conf import settings
from kavenegar import KavenegarAPI, APIException, HTTPException


def send_sms_token(phone_number: str, message: str) -> int:
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
