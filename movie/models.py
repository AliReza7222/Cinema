import uuid
from django.db import models

from accounts.models import UserSite
from .validators import check_name_word_and_number, is_number


class Room(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name_room = models.CharField(max_length=100, validators=[check_name_word_and_number], unique=True)
    quantity_person = models.PositiveIntegerField()
    address_room = models.TextField(blank=True, null=True)
    seat_reserved = models.TextField(validators=[is_number], default='0', editable=False)

    def __str__(self):
        return self.name_room


class Movie(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    permission_sell = models.BooleanField(default=True)
    image_movie = models.ImageField(upload_to='image_movie/')
    director_movie = models.CharField(max_length=150)
    price_ticket = models.CharField(max_length=10, validators=[is_number])
    genre_movie = models.CharField(max_length=100)
    room_movie = models.OneToOneField(Room, on_delete=models.CASCADE)
    name_movie = models.CharField(max_length=100, validators=[check_name_word_and_number])
    time_movie = models.TimeField()
    datetime_start = models.DateTimeField()
    about_movie = models.TextField(blank=True, null=True)
    registered_ticket = models.PositiveIntegerField(default=0, editable=False)

    def delete(self, using=None, keep_parents=False):
        self.image_movie.storage.delete(str(self.image_movie.name))
        super().delete()

    def __str__(self):
        return self.name_movie


class TicketMovie(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user_client = models.ForeignKey(UserSite, on_delete=models.CASCADE)
    movie_ticket = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10, validators=[is_number])
    datetime_bought = models.DateTimeField(auto_now=True)
    key_data = models.CharField(max_length=50, unique=True)
    encode_data = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.user_client}--{self.movie_ticket}'