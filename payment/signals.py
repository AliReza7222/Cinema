from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Transactions, Payment


@receiver(post_save, sender=Transactions)
def create_payment(sender, instance, created, **kwargs):
    if created:
        data = {
            "status": 201,
            'transaction_id': instance,
            'movie_id': instance.movie_id,
            'amount': instance.amount
        }
        Payment.objects.create(**data)
