from rest_framework import serializers
from ..models import Movie, Actor, Review

class movieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title','overview',)


class movieSerializer(serializers.ModelSerializer):

    class actorSerializer(serializers.ModelSerializer):
        class Meta:
            model = Actor
            fields = ('name',)

    class reviewListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Review
            fields = ('title','content',)
    
    actors = actorSerializer(many=True, read_only=True)
    reviews = reviewListSerializer(many=True, read_only=True, source = 'review_set')

    class Meta:
        model = Movie
        fields = '__all__'