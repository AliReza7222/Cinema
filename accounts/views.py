from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from .serializrs import SignUpSerializers


class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializers
