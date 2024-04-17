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
    user_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    username = None
    email = None

    EMAIL_FIELD = None
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = UserSiteManager()

    class Meta:
        db_table = 'user_site'

    def __str__(self):
        return self.phone_number


class ProfileUser(models.Model):
    user = models.OneToOneField(UserSite, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    photo = models.ImageField(upload_to='images/profile/', blank=True)

    class Meta:
        db_table = 'profile_user'

    def delete(self, using=None, keep_parents=False, *args, **kwargs):
        if self.photo:
            self.photo.storage.delete(str(self.photo.name))
        return super(ProfileUser, self).delete(*args, **kwargs)

    def __str__(self):
        return f"{self.user}"
