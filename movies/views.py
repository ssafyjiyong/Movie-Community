from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from .models import Movie, Comment
from .forms import MovieForm, CommentForm, SonCommentForm


# 전체 영화 데이터 조회 
@require_GET
def index(request):
    movies = Movie.objects.all().order_by('-pk')
    context = {
        'movies':movies,
    }
    return render(request, 'movies/index.html', context)

# 영화 데이터 작성 폼 출력
# 유효성 검증 및 영화 데이터 저장
@require_http_methods(['GET','POST'])
@login_required
def create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            form.save()
            return redirect('movies:index')
    else:
        form = MovieForm()
    context = {
        'form':form,
    }
    return render(request, 'movies/create.html', context)

# 단일 영화 데이터 및 댓글 목록 조회
# 댓글 작성 폼 출력 
@require_GET
def detail(request, pk):
    movie = Movie.objects.get(pk=pk)
    comment_form = CommentForm()
    soncomment_form=SonCommentForm()
    # comment_set은 모델의 Comment : 소문자로 쓰는게 규칙(자동인식)
    comments = movie.comment_set.all().order_by('-pk')
    context = {
        'movie':movie,
        'comment_form':comment_form,
        'comments':comments,
        'soncomment_form':soncomment_form,
    }
    return render(request, 'movies/detail.html', context)

# 영화 데이터 수정 페이지 조회 
# 유효성 검증 및 영화 데이터 수정  
@require_http_methods(['GET','POST'])
@login_required
def update(request, pk):
    movie = Movie.objects.get(pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            movie = form.save()
            return redirect('movies:detail', movie.pk)
    else:
        form = MovieForm(instance=movie)
    context = {
        'movie':movie,
        'form':form,
    }
    return render(request, 'movies/update.html', context)

# 단일 영화 데이터 삭제 
@require_POST
@login_required
def delete(request, pk):
    movie = Movie.objects.get(pk=pk)
    if request.user == movie.user:
        movie.delete()
    return redirect('movies:index')

@login_required
def comment_create(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.movie = movie
        comment_form.save()
        return redirect('movies:detail', movie.pk)
    context = {
        'movie':movie,
        'comment_form':comment_form,
    }
    return render(request, 'movies/index.html', context)

@login_required
def soncomment(request, movie_pk, comment_pk):
    movie = Movie.objects.get(pk=movie_pk)
    comment = Comment.objects.get(pk=comment_pk)
    soncomment_form=SonCommentForm(request.POST)
    if soncomment_form.is_valid():
        soncomment = soncomment_form.save(commit=False)
        soncomment.user = request.user
        soncomment.movie = movie
        soncomment.papa_comment = comment
        soncomment_form.save()
        return redirect('movies:detail', movie.pk)
    context = {
        'soncomment':soncomment,
        'soncomment_form':soncomment_form,
    }
    return render(request, 'movies/index.html', context)

@login_required
def comment_delete(request, movie_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('movies:detail', movie_pk)


@require_POST
def likes(request, movie_pk):
    if request.user.is_authenticated:
        movie = Movie.objects.get(pk=movie_pk)
        if movie.like_user.filter(pk=request.user.pk).exists():
            movie.like_user.remove(request.user)
        else:
            movie.like_user.add(request.user)
        return redirect('movies:index')
    return redirect('accounts:login')


@login_required
def cocomment_delete(request, movie_pk, cocomment_pk):
    cocomment = Comment.objects.get(pk=cocomment_pk)
    if request.user == cocomment.user:
        cocomment.delete()
    return redirect('movies:detail', movie_pk)
