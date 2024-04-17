from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserSite, ProfileUser


@receiver(post_save, sender=UserSite)
def create_profile_user(sender, instance, created, **kwargs):
    if created:
        ProfileUser.objects.create(user=instance)
