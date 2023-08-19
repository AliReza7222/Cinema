from rest_framework import serializers

from .models import Room


class RecordRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = [
            'name_room',
            'quantity_person',
            'address_room'
        ]
