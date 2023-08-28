import uuid
from django.db import models

from .validators import check_name_word_and_number, is_number


class Room(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name_room = models.CharField(max_length=100, validators=[check_name_word_and_number], unique=True)
    quantity_person = models.PositiveIntegerField()
    address_room = models.TextField(blank=True, null=True)

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
    registered_ticket = models.PositiveIntegerField(default=0)

    def delete(self, using=None, keep_parents=False):
        self.image_movie.storage.delete(str(self.image_movie.name))
        super().delete()

    def __str__(self):
        return self.name_movie


class TicketMovie(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    datetime_bought = models.DateTimeField()
    key_data = models.CharField(max_length=50, unique=True)
    encode_data = models.TextField()

    def __str__(self):
        return f'{self.key_data}'
