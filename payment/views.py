from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import TransactionsSerializer
from .models import Payment, Transactions
from .permissions import IsPermissionRegisterTicket
from movie.models import Movie, TicketMovie
from movie.utils import encode_data


class TransactionsView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsPermissionRegisterTicket]
    serializer_class = TransactionsSerializer

    def create_ticket_movie(self, user, movie, datetime_bought, transaction_id):
        payment_id = Transactions.objects.get(id=transaction_id).payment.id
        data_ticket = {
            'user_client': user.phone_number,
            'name_movie': movie.name_movie,
            'datetime_bought': str(datetime_bought.strftime('%Y-%m-%d %H:%M:%S')),
            'payment_id': str(payment_id)
        }
        data_encode, key = encode_data(data_ticket)
        TicketMovie.objects.create(key_data=key, encode_data=data_encode, movie=movie, datetime_bought=datetime_bought)
        return key

    def post(self, request, *args, **kwargs):
        data_post = request.data
        user = request.user
        movie_id = kwargs.get('movie_id')
        movie = Movie.objects.get(id=movie_id)
        # if you are developing project set "link_back": 'http://127.0.0.1/home/'
        amount = movie.price_ticket
        data = {
            'amount': amount,
            "link_back": 'http://127.0.0.1/home/',
            "email_client": data_post.get('email_client', None),
            "full_name_client": data_post.get('full_name_client', None)
        }
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            obj_transaction = serializer.save(user=user, movie_id=movie)
            key = self.create_ticket_movie(user=user, movie=movie,
                                           datetime_bought=obj_transaction.datetime_transactions,
                                           transaction_id=obj_transaction.id)
            data_json = serializer.data
            data_json['ticket_key'] = key
            return Response(data=data_json, status=status.HTTP_201_CREATED)

        # create a payment failure
        Payment.objects.create(
            user=user, movie_id=movie_id,
            amount=amount, status=400
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
