from rest_framework import serializers
from .models import Review, Comment

class reviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('title','content',)


class reviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class commentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'