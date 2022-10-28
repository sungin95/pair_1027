from .models import Review, Comment
from django import forms


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            "title",
            "content",
            "movie_name",
            "grade",
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
