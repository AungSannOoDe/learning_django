from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Phone number is required")

        user = self.model(
        phone_number=phone_number,
        **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(
        phone_number=phone_number,
        password=password,
        **extra_fields
    )
class User(AbstractUser):
    username = None
    email=None
    phone_number = models.CharField(
        max_length=20,
        unique=True
    )

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["first_name"]
    objects = UserManager()

    def __str__(self):
        return self.phone_number


class Movie(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    review = models.FloatField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class StreamPlatform(models.Model):
    name = models.CharField(max_length=10)
    about = models.CharField(max_length=20)
    website = models.URLField(max_length=50)

    def __str__(self):
        return self.name


class WatchList(models.Model):
    title = models.CharField(max_length=10)
    storyline = models.CharField(max_length=200)

    platform = models.ForeignKey(
        StreamPlatform,
        on_delete=models.CASCADE,
        related_name="watchlist"
    )

    average_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    review_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    ratings = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    description = models.CharField(
        max_length=200,
        null=True
    )

    watchlist = models.ForeignKey(
        WatchList,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.ratings) + " " + self.watchlist.title