from django.urls import path

from .views import TransactionsView


app_name = 'payment'
urlpatterns = [
    path('payment/<uuid:movie_id>/', TransactionsView.as_view(), name='transaction')
]
