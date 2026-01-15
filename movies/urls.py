from django.urls import path, include
from .views import movie_list, movie_detail, search_view

app_name = "movies"

urlpatterns = [
    path("", movie_list, name="movie_list"),
    path("<int:movie_id>/", movie_detail, name="movie_detail"),
    path("search/", search_view, name="search"),
]
