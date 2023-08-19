from django.urls import path
from .views import RecordRoomView, RecordMovieView


urlpatterns = [
    path('record_room/', RecordRoomView.as_view(), name='record_room'),
    path('record_movie/', RecordMovieView.as_view(), name='record_movie')
]
