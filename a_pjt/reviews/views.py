from django.shortcuts import render, redirect
from .models import Review
from .forms import Commentform,Reviewform
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    reviews = Review.objects.order_by('-pk')
    context = {
        'reviews':reviews
    }
    return render(request, 'reviews/index.html', context)

def detail(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    commet_form = Commentform()
    context={
        'review':review,
        'comment_form':commet_form,
        'comments':review.commet_set.all(),
    }
    return render(request, 'reviews/detail.html',context)

def create(requsest):
    pass

def comment_create(request, pk):
    review = Review.objects.get(pk=pk)
    comment_form = Commentform(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user 
        comment.save()
    return redirect('reviews:detail', review.pk )

def comment_delete(request, review_pk, comment_pk):
    comment = Commentform.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('reviews:detail', review_pk)

# @login_required
def create(request):
    if request.method == "POST":
        form = Reviewform(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
        return redirect('reviews:create')
    else:
        form = Reviewform()
    context={
        'form':form
    }
    return render(request, 'reviews/create.html',context)
