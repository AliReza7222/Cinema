from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import TransactionsSerializer
from movie.models import Movie


class TransactionsView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionsSerializer

    def post(self, request, *args, **kwargs):
        data_post = request.data
        user = request.user
        movie_id = kwargs.get('movie_id')
        movie = Movie.objects.filter(id=movie_id)
        if not movie:
            message = '! فیلمی پیدا نشد احتمالا در شناسایی فیلم مشکلی پیش اومده '
            return Response({'error_message': message}, status=status.HTTP_404_NOT_FOUND)
        # if you are developing project set "link_back": 'http://127.0.0.1/home/'
        amount = movie.first().price_ticket
        data = {
            'amount': amount,
            "link_back": 'http://127.0.0.1/home/',
            "email_client": data_post.get('email_client', None),
            "full_name_client": data_post.get('full_name_client', None)
        }
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user, movie_id=movie.first())
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
