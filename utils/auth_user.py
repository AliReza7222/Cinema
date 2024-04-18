import random
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from string import ascii_uppercase, ascii_lowercase, digits

from accounts.models import UserSite, ProfileUser


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


def login_user(phone_number: str = None, user: UserSite = None) -> dict:
    if phone_number and not user:
        user = get_object_or_404(UserSite, phone_number=phone_number)
    data_profile = ProfileUser.objects.filter(user=user).values().first()
    refresh = RefreshToken.for_user(user)
    return {
        'tokens': {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        },
        'user-uuid': user.user_uuid,
        'profile-user': data_profile
    }
