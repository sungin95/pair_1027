from django.shortcuts import render
from .models import Review
from .forms import Commetform
# Create your views here.

def detail(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    commet_form = Commetform()
    context={
        'review':review,
        'comment_form':commet_form,
        'comments':review.commet_set.all(),
    }
    return render(request, 'reviews/detail.html',context)