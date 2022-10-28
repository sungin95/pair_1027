from django.shortcuts import render, redirect
from .models import Review, Comment
from .forms import CommentForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.


def index(request):
    reviews = Review.objects.order_by("-pk")
    context = {"reviews": reviews}
    return render(request, "reviews/index.html", context)


def detail(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    comment_form = CommentForm()
    context = {
        "review": review,
        "comment_form": comment_form,
        "comments": review.comment_set.all(),
    }
    return render(request, "reviews/detail.html", context)


@login_required
def like(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if review.like.filter(pk=request.user.pk).exists():
        review.like.remove(request.user)
        is_like = False
    else:
        review.like.add(request.user)
        is_like = True
    context={
        'is_like':is_like,
        'liketCount': review.like.count(),
    }
    return JsonResponse(context)


def comment_create(request, pk):
    review = Review.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
        context = {
            'comment': comment.content,
            'userName': comment.user.username,
            'commentPk': comment.pk,
        }
        return JsonResponse(context)
    

def comment_delete(request, review_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect("reviews:detail", review_pk)


@login_required
def create(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
        return redirect("reviews:index")
    else:
        form = ReviewForm()
    context = {"form": form}
    return render(request, "reviews/create.html", context)


@login_required
def update(request, pk):
    reviews = Review.objects.get(pk=pk)
    if request.user == reviews.user:
        if request.method == "POST":
            form = ReviewForm(request.POST, request.FILES, instance=reviews)
            if form.is_valid():
                form.save()
                messages.success(request, "글 수정을 완료 했습니다.")
                return redirect("reviews:detail", reviews.pk)
        else:
            form = ReviewForm(instance=reviews)
        context = {"form": form}
        return render(request, "reviews/update.html", context)


def delete(request, pk):
    reviews = Review.objects.get(pk=pk)
    if request.user == reviews.user:
        reviews.delete()
    return redirect("reviews:index")
