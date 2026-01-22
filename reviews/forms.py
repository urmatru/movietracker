from django import forms
from .models import Review, Comment

class AddReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment 
        fields = ("text",)
        labels = {'text': ''}
        widgets = {
            "text": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Write a comment..."
            })
        }
        