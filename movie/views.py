from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .permissions import IsSuperUser
from .serializers import RecordRoomSerializer, RecordMovieSerializer


class RecordRoomView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsSuperUser]
    serializer_class = RecordRoomSerializer


class RecordMovieView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsSuperUser]
    serializer_class = RecordMovieSerializer
