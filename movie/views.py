from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .permissions import IsSuperUser
from .utils import decode_data
from .models import Movie, Room, TicketMovie
from .serializers import RecordRoomSerializer, RecordMovieSerializer, GetKeyTicketMovieSerializer


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


class DecodeDataTicket(APIView):
    permission_classes = [IsAuthenticated, IsSuperUser]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = GetKeyTicketMovieSerializer(data=data)
        if serializer.is_valid():
            key_data = serializer.validated_data.get('key_data')
            ticket_movie = TicketMovie.objects.get(key_data=key_data)
            data_ticket = decode_data(ticket_movie.encode_data, key_data)
            return Response(data=data_ticket, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
