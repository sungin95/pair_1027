from django.shortcuts import render, redirect
from .models import Review, Comment
from .forms import Commentform,Reviewform
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
        'comments':review.comment_set.all(),
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

def comment_delete(request, review_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
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
        return redirect('reviews:index')
    else:
        form = Reviewform()
    context={
        'form':form
    }
    return render(request, 'reviews/create.html',context)

@login_required
def update(request, pk):
    reviews = Review.objects.get(pk=pk)
    if request.method == "POST":
        form = Reviewform(request.POST, request.FILES, instance=reviews)
        if form.is_valid():
            form.save()
            messages.success(request, '글 수정을 완료 했습니다.')
            return redirect('reviews:detail', reviews.pk)
    else:
        form = Reviewform(instance=reviews)
    context = {
        'form': form
    }
    return render(request, 'reviews/update.html', context)