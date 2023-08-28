from rest_framework.permissions import BasePermission

from movie.models import Movie


class IsPermissionRegisterTicket(BasePermission):

    def has_permission(self, request, view):
        movie_id = view.kwargs.get('movie_id')
        movie = Movie.objects.filter(id=movie_id)
        # if uuid invalid can't use this view !
        if not movie:
            return False

        # permission sell ticket
        movie = movie.first()
        return movie.permission_sell
