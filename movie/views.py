from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .permissions import IsSuperUser
from .serializers import RecordRoomSerializer


class RecordRoomView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsSuperUser]
    serializer_class = RecordRoomSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data_response = serializer.data
        data_response['message'] = f"اتاق {data_response.get('name_room')}  توسط کاربر ادمین {request.user} ایجاد شد ! "
        return Response(data_response, status=status.HTTP_201_CREATED, headers=headers)
