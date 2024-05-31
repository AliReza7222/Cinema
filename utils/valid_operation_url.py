from accounts.models import UserSite
from TheCinema import response_msg as msg


def invalid_operation(op: str) -> dict:
    operations = ('register', 'login', 'forget_password')
    if op not in operations:
        return {'message': msg.ERROR_INVALID_URL, 'type': 'error'}
    return None


def check_operation_view(op: str, phone_number: str) -> dict:
    find_number = UserSite.objects.filter(phone_number=phone_number)
    if op == 'register' and find_number.exists():
        return {'message': msg.ERROR_DUPLICATE_PHONE_NUMBER, 'type': 'error'}
    elif op in ('login', 'forget_password') and not find_number.exists():
        return {'message': msg.ERROR_NOT_EXISTS_PHONE_NUMBER, 'type': 'error'}
    else:
        return None
