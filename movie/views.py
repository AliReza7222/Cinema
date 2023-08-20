from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .permissions import IsSuperUser
from .utils import encode_data
from .models import Movie, Room
from .serializers import RecordRoomSerializer, RecordMovieSerializer


class RecordRoomView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsSuperUser]
    serializer_class = RecordRoomSerializer


class RecordMovieView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsSuperUser]
    serializer_class = RecordMovieSerializer


class ShowAllRoom(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        rooms = Room.objects.values()
        data = dict()
        for room in rooms:
            data[room.get('name_room')] = room
        return Response(data, status=status.HTTP_200_OK)


class ShowAllMovie(ListAPIView):

    def get(self, request, *args, **kwargs):
        movies = Movie.objects.values()
        data = dict()
        for movie in movies:
            data[movie.get('name_movie')] = movie
        return Response(data, status=status.HTTP_200_OK)

