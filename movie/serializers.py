from rest_framework import serializers

from .models import Room, Movie


class RecordRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = [
            'id',
            'name_room',
            'quantity_person',
            'address_room'
        ]


class RecordMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'name_movie',
            'genre_movie',
            'director_movie',
            'time_movie',
            'datetime_start',
            'price_ticket',
            'room_movie',
            'image_movie',
            'about_movie'
        ]
