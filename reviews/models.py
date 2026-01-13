from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from movies.models import Movie

# Create your models here.

User = settings.AUTH_USER_MODEL

class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_reviews"
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="movie_reviews"
    )

    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "movie")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} -> {self.movie} ({self.rating})"