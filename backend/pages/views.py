from django.shortcuts import render
from reviews.models import Review

# Create your views here.
def home(request):
    recent_reviews = Review.objects.select_related('movie', 'user').order_by('-created_at')[:10]

    context = {
        "recent_reviews" : recent_reviews
    }
    return render(request, "home.html", context)