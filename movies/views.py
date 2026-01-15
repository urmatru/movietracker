from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Count
from movies.services.omdb import OMDBClient
from .models import Movie
# Create your views here.

def movie_list(request):
    movies = Movie.objects.annotate(
        num_reviews=Count('movie_reviews'),
        avg_rating=Avg('movie_reviews__rating'),
    ).filter(
        num_reviews__gt=0
    ).order_by(
        '-avg_rating'
    )

    return render(request, "movies/movie_list.html", {"movies": movies})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = movie.movie_reviews.all()
    return render(
        request, 
        "movies/movie_detail.html",
        {"movie": movie, "reviews": reviews}
    )

def search_view(request):
    query = request.GET.get("q")
    movie = None
    reviews = []

    if query:
        client = OMDBClient()
        result = client.search_movie(query)
        movies_data = result.get("Search", [])
        
        if movies_data:
            data = movies_data[0]
            movie, created = Movie.objects.get_or_create(
                external_id=data["imdbID"],
                defaults={
                    "title": data["Title"],
                    "description": data.get("Plot", ""),
                    "year": int(data["Year"]) if data["Year"].isdigit() else None,
                    "poster": data.get("Poster", "")
                }
            )
            reviews = movie.movie_reviews.all()

    context = {
        "movie": movie,
        "reviews": reviews,
        "query": query,
    }

    return render(
        request, 
        "movies/movie_detail.html",
        context
    )

