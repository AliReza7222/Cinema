from django.urls import path

from .views import (
    SignUpView,
    CheckInformationUserView,
    CheckTokenView,
    ChangePasswordView
)


app_name = 'accounts'
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='sign_up'),
    path('signin/check_info_user/', CheckInformationUserView.as_view(), name='check_info_user'),
    path('signin/check_token/<uuid:user_uuid>/', CheckTokenView.as_view(), name='check_token'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password')
]
