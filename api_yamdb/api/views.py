from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_201_CREATED
from rest_framework.viewsets import  ModelViewSet
from django.core.mail import send_mail
import random 
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import CustomUser, Title, Genre, Category
from .serializers import (
                    TitleSerializer, CategorySerializer,
                    GenreSerializer, SignupSerializer, 
                    CustomUsersSerializer, TokenSerializer
    )
from .permission import IsAdmin, ReadOnly
from .pagination import Pagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdmin,)

    def get_permissions(self):
        if self.action == 'list':
            return (ReadOnly(),)
        return super().get_permissions()


class APIsignup(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        email = data.get('email')
        confirmation_code = random.randint(100000, 999999)
        send_mail('Confirmation code',
            f'Your code for getting a token - {confirmation_code}.',
            settings.DEFAULT_EMAIL,
            [email,],
            fail_silently=False,)
        serializer.save()
        return Response(serializer.validated_data, status=HTTP_200_OK)


class APIgetToken(APIView):

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            email = data.get('email')
            confirmation_code = data.get('confirmation_code')
            user = get_object_or_404(CustomUser, email=email, confirmation_code=confirmation_code)
            if user:
                try:
                    token = RefreshToken.for_user(user).access_token
                    return Response({'token': str(token)}, status=HTTP_201_CREATED)
                except Exception as error:
                    raise error
            else:
                result = {
                    'error': 'Can not authenticate with the given credentials'}
                return Response(result, status=HTTP_403_FORBIDDEN)
        except KeyError:
            result = {'error': 'Please provide a email and a confirmation code'}
            return Response(result)


class APIusers(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUsersSerializer
    pagination_class = Pagination
    permission_classes = (IsAdmin,)
