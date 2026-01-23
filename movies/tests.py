from django.test import TestCase
from django.core.exceptions import ValidationError
from movies.models import Movie
# Create your tests here.

class MovieModelTest(TestCase):
    def test_create_valid_movie(self):
        movie = Movie.objects.create(
            title="Inception",
            year=2010,
            description='Horror film for kids',
            poster="http://example.com/poster.jpg",
            external_id="tt13132490"
        )
        self.assertEqual(movie.title, "Inception")
        self.assertEqual(str(movie), "Inception (2010)")

    def test_movie_title_max_length(self):
        movie = Movie(title="A" * 256, year=2023)
        with self.assertRaises(ValidationError):
            movie.full_clean()

  