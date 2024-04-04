from django.urls import path

from .views import (
    SignUpView,
    StepOneSignInView,
    ChangePasswordView
)


app_name = 'accounts'
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='sign_up'),
    path('signin/1/', StepOneSignInView.as_view(), name='step_one_signin'),
    path('change_password/<str:step>/', ChangePasswordView.as_view(), name='change_password')
]
