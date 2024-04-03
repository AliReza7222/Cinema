from django.urls import path

from .views import SignUpView, SignInView, RefreshTokenView, ChangePasswordView


app_name = 'accounts'
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='sign_up'),
    path('signin/<str:step>/', SignInView.as_view(), name='signin'),
    path('refresh_token/', RefreshTokenView.as_view(), name='refresh'),
    path('change_password/<str:step>/', ChangePasswordView.as_view(), name='change_password')
]
