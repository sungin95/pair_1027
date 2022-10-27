from django.shortcuts import render, redirect
from .models import Review
from .forms import CommentForm
# Create your views here.

################################################################
######## detail 페이지 구현시 참고 댓글 목록 조회 쿼리 ##########
################################################################
# def detail(request, pk):
#     reviews = Reviews.objects.get(pk=pk)
#     comment_form = CommentForm()
#     comments = reviews.comment_set.all()
#     context = {
#         'reviews': reviews,
#         'comment_form': comment_form,
#         'comments':comments,
#     }
#     return render(request, 'reviews/detail.html', context)

def comment_create(request, pk):
    review = Review.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user 
        comment.save()
    return redirect('reviews:detail', review.pk )

def comment_delete(request, article_pk, comment_pk):
    comment = CommentForm.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('reviews:detail', article_pk)