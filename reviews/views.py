from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AddReviewForm
from django.contrib import messages
from movies.models import Movie
from movies.services.omdb import OMDBClient


# Create your views here.

@login_required
def add_review(request):
    movie = None
    query = request.GET.get("q")
    if query:
        # сначала ищем в базе
        movie = Movie.objects.filter(title__icontains=query).first()
        if not movie:
            try:
                client = OMDBClient()
                result = client.search_movie(query)
                movies_data = result.get("Search", [])
                if movies_data:
                    data = movies_data[0]
                    movie, created = Movie.objects.get_or_create(
                        external_id=data["imdbID"],
                        defaults={
                            "title": data["Title"],
                            "description": "",
                            "year": int(data["Year"]) if data["Year"].isdigit() else None,
                            "poster": data.get("Poster", "")
                        }
                    )
                else: 
                    print("No Search in OMDB result")
            except Exception as e:
                print("OMDB Error:", str(e))
                raise
                 
    if request.method == "POST":
        form = AddReviewForm(request.POST)
        if form.is_valid() and movie:
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            try: 
                review.save()
                messages.success(request, 
                f"'{movie.title}'добавлен в список ваших фильмов!"
                )
            except:
                messages.error(request, "Вы уже добавили этот фильм.")
            return redirect('users:profile')
        
    else: 
        form = AddReviewForm()

    return render(request, "reviews/add_review.html", {
        "form": form,
        "movie": movie,
        "query": query,
    })

