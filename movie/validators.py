import re
from rest_framework.exceptions import ValidationError


def check_name_word_and_number(value):
    pattern = r'^[\w\s]+$'
    match = re.match(pattern, value)

    if match is None:
        raise ValidationError('Name must contain words and numbers!')

    return value
