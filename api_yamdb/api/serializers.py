from rest_framework import serializers
from reviews.models import CustomUser, Title, Genre, Category


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
        model = CustomUser
        fields = ('email', 'username',)


class CustomUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code')