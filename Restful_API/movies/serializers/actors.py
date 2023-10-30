from rest_framework import serializers
from ..models import Actor, Movie

class actorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'


class actorSerializer(serializers.ModelSerializer):

    class movieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('title',)

    movies = movieSerializer(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = ('pk','name','movies',)