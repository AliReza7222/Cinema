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
    path('auth/<str:op>_op/<str:phone_number>/', CheckTokenView.as_view(), name='check_token'),
    path('auth/login/with_password/', LoginWithPasswordView.as_view(), name='login_with_password'),
    path('setـpassword/', CompleteAuthentication.as_view(), name='set_password'),
    path('completeـprofile/', CompleteProfileView.as_view(), name='complete_profile'),
    path('changeـpassword/', ChangePasswordView.as_view(), name='change_password'),
]
