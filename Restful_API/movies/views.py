from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers.actors import actorListSerializer, actorSerializer
from .serializers.movies import movieListSerializer, movieSerializer
from .serializers.reviews import reviewListSerializer, reviewSerializer
from .models import Actor, Movie, Review

# Create your views here.
@api_view(['GET'])
def actors_list(request):
    actors = get_list_or_404(Actor)
    serializer = actorListSerializer(actors, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def actor_detail(request, actor_pk):
    actor = get_object_or_404(Actor, pk=actor_pk)
    serializer = actorSerializer(actor)
    return Response(serializer.data)

@api_view(['GET'])
def movies_list(request):
    movies = get_list_or_404(Movie)
    serializer = movieListSerializer(movies, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = movieSerializer(movie)
    return Response(serializer.data)

@api_view(['GET'])
def reviews_list(request):
    reviews = get_list_or_404(Review)
    serializer = reviewListSerializer(reviews, many = True)
    return Response(serializer.data)

@api_view(['GET','PUT','DELETE'])
def review_detail(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'GET':
        serializer = reviewSerializer(review)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = reviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(f'message : review {review_pk} is deleted', status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def review_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = reviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
