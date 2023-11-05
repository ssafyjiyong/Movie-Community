from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_safe
from django.core import serializers
from .models import Movie, Genre

# Create your views here.
@require_safe
def index(request):
    top_movies = []
    for i in range(5):
        top_movies.append(Movie.objects.all().order_by('-popularity')[i])
    movie1 = top_movies[0]
    movie2 = top_movies[1]
    movie3 = top_movies[2]
    movie4 = top_movies[3]
    movie5 = top_movies[4]
    movies = Movie.objects.all().order_by('-release_date')
    context = {
        'movies':movies,
        'top_movies':top_movies,
        'movie1':movie1,
        'movie2':movie2,
        'movie3':movie3,
        'movie4':movie4,
        'movie5':movie5,
    }
    return render(request, 'movies/index.html', context)


@require_safe
def detail(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    movie_genre = movie.genres.all()

    try:
        prv_movie = Movie.objects.filter(release_date__lt=movie.release_date).order_by('-release_date')[0]
    except IndexError:
        prv_movie_pk = -99
    else:
        prv_movie_pk = prv_movie.pk

    try:
        nxt_movie = Movie.objects.filter(release_date__gt=movie.release_date).order_by('release_date')[0]
    except IndexError:
        nxt_movie_pk = -99
    else:
        nxt_movie_pk = nxt_movie.pk

    context = {
        'prv_movie_pk': prv_movie_pk,
        'nxt_movie_pk': nxt_movie_pk,
        'movie': movie,
        'movie_genre': movie_genre,
    }
    return render(request, 'movies/detail.html', context)


@require_safe
def recommended(request):
    movies = Movie.objects.all().order_by('-release_date')
    genres = Genre.objects.all()
    context = {
        'movies': movies,
        'genres': genres,
    }
    return render(request, 'movies/recommended.html', context)


@require_safe
def select_genre(request, genre_pk):
    genre = get_object_or_404(Genre, pk=genre_pk)
    movies = Movie.objects.filter(genres=genre).order_by('-release_date')
    movie_list = []
    for movie in movies:
        movie_info = {
            'pk': movie.pk,
            'title': movie.title,
            'poster_path': movie.poster_path,
            'release_date': movie.release_date,
            'genres': [genre.name for genre in movie.genres.all()],
            'vote_average': movie.vote_average,
            'overview': movie.overview,
        }
        movie_list.append(movie_info)
    
    context = {
        'movies': movie_list,
        'genre': genre.name,
    }
    return JsonResponse(context)

