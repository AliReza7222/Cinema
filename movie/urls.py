from django.urls import path
from .views import RecordRoomView


urlpatterns = [
    path('record_room/', RecordRoomView.as_view(), name='record_room')
]
