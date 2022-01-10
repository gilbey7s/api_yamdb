from rest_framework import serializers

from reviews.models import CustomUser


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
