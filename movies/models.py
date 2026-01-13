from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title