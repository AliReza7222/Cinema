from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Transactions, Payment


@receiver(post_save, sender=Transactions)
def create_payment(sender, instance, created, **kwargs):
    movie = instance.movie_id
    if created:
        # create a payment wit status 201
        data = {
            "status": 201,
            'transaction_id': instance,
            'movie_id': movie,
            'amount': instance.amount,
            'date_payment': instance.datetime_transactions
        }
        Payment.objects.create(**data)
        # client user registered in room movie .
        room = movie.room_movie
        if room.quantity_person > movie.registered_ticket:
            movie.registered_ticket += 1
            if room.quantity_person == movie.registered_ticket:
                movie.permission_sell = False
            movie.save()
