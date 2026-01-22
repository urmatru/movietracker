from django.urls import path
from .views import add_review, add_comment, delete_comment

app_name = "reviews"

urlpatterns = [
    path("add/", add_review, name="add_review"),
    path("add_comment/<int:review_id>/", add_comment, name="add_comment"),
    path("add_comment/<int:comment_id>/delete/", delete_comment, name="delete_comment"),
]