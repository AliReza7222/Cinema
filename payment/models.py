import uuid
from django.db import models

from movie.models import Movie
from accounts.models import UserSite


class Transactions(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    movie_id = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(UserSite, on_delete=models.SET_NULL, null=True)
    full_name_client = models.CharField(max_length=150, null=True, blank=True)
    amount = models.CharField(max_length=10)
    email_client = models.EmailField(null=True, blank=True)
    datetime_transactions = models.DateTimeField(auto_now=True)
    link_back = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.user}   /   {self.datetime_transactions}   /   {self.amount}$'


class Payment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=True, primary_key=True)
    status = models.PositiveIntegerField(editable=False)
    transaction_id = models.ForeignKey(Transactions, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True)
    amount = models.CharField(max_length=10)
    date_payment = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.amount}/{self.date_payment}/{self.status}'


