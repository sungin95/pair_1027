from dataclasses import fields
from .models import Review, Comment
from django import forms

class Reviewform(forms.ModelForm):
    class meta:
        model= Review
        fields= ['title','content','movie_name','grade',] 


class Commentform(forms.ModelForm):
    class meta:
        model= Comment
        fields= ['content'] 

