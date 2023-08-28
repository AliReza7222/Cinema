from django.contrib import admin

from .models import Room, Movie, TicketMovie


admin.site.register(Room)
admin.site.register(Movie)
admin.site.register(TicketMovie)
