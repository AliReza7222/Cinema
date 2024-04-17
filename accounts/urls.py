from django.urls import path

from .views import (
    CheckTokenView,
    ChangePasswordView,
    GetPhoneNumberView,
    CompleteAuthentication,
    CompleteProfileView,
    LoginWithPasswordView
)


app_name = 'accounts'
urlpatterns = [
    path('auth/<str:op>/', GetPhoneNumberView.as_view(), name='login_register'),
    path('auth/<str:op>/<str:phone_number>/', CheckTokenView.as_view(), name='check_token'),
    path('set_password/', CompleteAuthentication.as_view(), name='set_password'),
    path('complete_profile/', CompleteProfileView.as_view(), name='complete_profile'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('auth/login/password/<str:phone_number>/', LoginWithPasswordView.as_view(), name='login_with_password'),
]
