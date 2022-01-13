from rest_framework import serializers
<<<<<<< HEAD
from reviews.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ("id", "text",
                  "author", "score", "pub_date",)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )

    class Meta:
        model = Comment
        fields = (
            "id", "text",
            "author", "pub_date",)
=======
from reviews.models import Title, Genre, Category
from django.contrib.auth import get_user_model


User = get_user_model()

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


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username',)


class CustomUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
>>>>>>> c8090dd55aab208a1e0ef760ca2302fc289b218c
