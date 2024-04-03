from django.urls import path
from .views import RecordRoomView, RecordMovieView, ShowAllMovie, ShowAllRoom, DecodeDataTicket


app_name = 'movie'
urlpatterns = [
    path('record_room/', RecordRoomView.as_view(), name='record_room'),
    path('record_movie/', RecordMovieView.as_view(), name='record_movie'),
    path('movies/', ShowAllMovie.as_view(), name='movies'),
    path('rooms/', ShowAllRoom.as_view(), name='rooms'),
    path('decode_ticket/', DecodeDataTicket.as_view(), name='decode_ticket')
]
