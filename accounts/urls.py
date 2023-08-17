from django.urls import path

from .views import SignUpView, SignInView


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='sign_up'),
    path('signin/', SignInView.as_view(), name='signin')
]
