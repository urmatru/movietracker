from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import AddReviewForm
from django.contrib import messages
from movies.models import Movie
from movies.services.omdb import OMDBClient
from reviews.models import Review, Comment
from reviews.forms import CommentForm


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

@login_required
def add_comment(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = review 
            comment.author = request.user
            comment.save()
        
    return redirect("movies:movie_detail", review.movie.id)

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user:
        return HttpResponseForbidden("You can delete only your own comments")
    
    movie_id = comment.review.movie.id
    comment.delete()

    return redirect("movies:movie_detail", movie_id)