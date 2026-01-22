from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True
    )

    country = models.CharField(
        max_length=100,
        blank=True
    )

    country_code = models.CharField(
        max_length=2,
        blank=True,
        help_text="ISO code, e.g. US, RU, DE"
    )
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username