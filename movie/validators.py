import re
from rest_framework.exceptions import ValidationError


def check_name_word_and_number(value):
    pattern = r'^[\w\s]+$'
    match = re.match(pattern, value)

    if match is None:
        raise ValidationError('Name must contain words and numbers!')

    return value


def is_number(value):
    pattern = r'^[\d]+$'
    match = re.match(pattern, value)

    if match is None:
        raise ValidationError('This Field be must numbers !')
    return value
