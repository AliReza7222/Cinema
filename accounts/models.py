import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserSiteManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The PhoneNumber field must be set")

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, password, **extra_fields)


class UserSite(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = None
    email = None
    phone_number = models.CharField(max_length=11, unique=True)

    EMAIL_FIELD = None
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = UserSiteManager()

    def __str__(self):
        return self.phone_number
