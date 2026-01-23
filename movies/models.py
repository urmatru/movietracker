from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)

    poster = models.ImageField(
        upload_to="posters/",
        blank=True,
        null=True
    )

    external_id = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        help_text="ID фильма по внешнему API (TMDB)"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["year"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.year})" 
