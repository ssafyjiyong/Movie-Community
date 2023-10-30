from rest_framework import serializers
from ..models import Review, Movie

class reviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('title','content',)


class reviewSerializer(serializers.ModelSerializer):

    class movieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('title',)

    movie = movieSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'