from rest_framework import serializers

from .models import Transactions, Payment


class TransactionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transactions
        fields = '__all__'
        read_only_fields = [
            'id',
            'movie_id',
            'user',
            'datetime_transactions'
        ]


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = '__all__'
