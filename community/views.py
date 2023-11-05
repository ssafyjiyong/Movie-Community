from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import (
    require_safe,
    require_POST,
    require_http_methods,
)
from .models import Review, Comment
from .forms import ReviewForm, CommentForm, SonCommentForm


@require_safe
def index(request):
    reviews = Review.objects.order_by('-pk')
    context = {
        'reviews': reviews,
    }
    return render(request, 'community/index.html', context)


@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            form.save()
            return redirect('community:detail', review.pk)
    else:
        form = ReviewForm()
    context = {
        'form': form,
    }
    return render(request, 'community/create.html', context)


@require_safe
def detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comments = review.comment_set.all().order_by('-pk')
    only_comment_cnt = comments.filter(papa_comment__isnull=True).count()
    comment_form = CommentForm()
    soncomment_form=SonCommentForm()
    context = {
        'review': review,
        'comment_form': comment_form,
        'comments': comments,
        'soncomment_form':soncomment_form,
        'only_comment_cnt':only_comment_cnt,
    }
    return render(request, 'community/detail.html', context)


@require_POST
def create_comment(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment_form.save()
        return redirect('community:detail', review.pk)
    context = {
        'comment_form': comment_form,
        'review': review,
        'comments': review.comment_set.all(),
    }
    return render(request, 'community/detail.html', context)


@require_POST
def like(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    person = request.user
    if person in review.like_users.all():
        review.like_users.remove(person)
        is_liked = False
    else:
        review.like_users.add(person)
        is_liked = True
    context = {
        'is_liked':is_liked,
        'likes_count':review.like_users.count(),
    }
    return JsonResponse(context)


@login_required
def comment_delete(request, review_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    context = {
        'review_pk':review_pk,
        'comment_pk':comment_pk,
    }
    return JsonResponse(context)
# 댓글 삭제에는 딱히 JsonResponse로 보낼 값이 없는 것 같지만
# 비어 있으면 안될 것 같으니 pk라도 전달하자..


@login_required
def soncomment_create(request, review_pk, comment_pk):
    review = Review.objects.get(pk=review_pk)
    comment = Comment.objects.get(pk=comment_pk)
    soncomment_form=SonCommentForm(request.POST)
    if soncomment_form.is_valid():
        soncomment = soncomment_form.save(commit=False)
        soncomment.user = request.user
        soncomment.review = review
        soncomment.papa_comment = comment
        soncomment_form.save()
        return redirect('community:detail', review.pk)
    context = {
        'soncomment':soncomment,
        'soncomment_form':soncomment_form,
    }
    return render(request, 'community/index.html', context)


@login_required
def soncomment_delete(request, review_pk, soncomment_pk):
    cocomment = Comment.objects.get(pk=soncomment_pk)
    if request.user == cocomment.user:
        cocomment.delete()
    context = {
        'review_pk':review_pk,
        'soncomment_pk':soncomment_pk,
    }
    return JsonResponse(context)