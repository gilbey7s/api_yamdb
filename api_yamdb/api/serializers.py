from rest_framework import serializers

from ..reviews.models import Title, Genre, Category


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('category', 'genre', 'name', 'year')
        model = Title


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category

