from django.shortcuts import render, redirect
from .models import Review
from .forms import Commentform
# Create your views here.

def detail(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    commet_form = Commentform()
    context={
        'review':review,
        'comment_form':commet_form,
        'comments':review.commet_set.all(),
    }
    return render(request, 'reviews/detail.html',context)

def comment_create(request, pk):
    review = Review.objects.get(pk=pk)
    comment_form = Commentform(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user 
        comment.save()
    return redirect('reviews:detail', review.pk )

def comment_delete(request, article_pk, comment_pk):
    comment = Commentform.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('reviews:detail', article_pk)

