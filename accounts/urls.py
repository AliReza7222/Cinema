from django.urls import path

from .views import SignUpView, SignInView, RefreshTokenView


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='sign_up'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('refresh_token/', RefreshTokenView.as_view(), name='refresh')
]
