from django.urls import path

from .views import (
    SignUpView,
    CheckInformationUserView,
    CheckTokenView,
    ChangePasswordView,
    SendTokenForgetPasswordView,
    GetForgetPasswordView
)


app_name = 'accounts'
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='sign_up'),
    path('signin/check_info_user/', CheckInformationUserView.as_view(), name='check_info_user'),
    path('signin/check_token/<uuid:user_uuid>/', CheckTokenView.as_view(), name='check_token'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('forget_password/token/', SendTokenForgetPasswordView.as_view(), name='send_token_forget_password'),
    path('forget_password/set/<uuid:user_uuid>/', GetForgetPasswordView.as_view(), name='set_forget_password')
]
