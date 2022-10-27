
from .models import Review, Comment
from django import forms

class Reviewform(forms.ModelForm):
    class Meta:
        model= Review
        fields= ['title','content','movie_name','grade',] 


class Commentform(forms.ModelForm):
    class Meta:
        model= Comment
        fields= ['content'] 

