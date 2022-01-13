<<<<<<< HEAD
from reviews.models import Comment, Review
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .serializers import CommentSerializer, ReviewSerializer
from .permissions import ReviewCommentPermission
from .pagination import ReviewsPagination, CommentsPagination

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = ReviewCommentPermission
    pagination_class = ReviewsPagination

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id) #тайтл надо дописать
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        if Review.objects.filter(
                author=self.request.user, title=title).exists():
            raise ValidationError("Вы уже оставляли отзыв на это произведение")
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [ReviewCommentPermission]
    pagination_class = CommentsPagination

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id)
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id, title__pk=title_id)
        serializer.save(author=self.request.user, review=review)
=======
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
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from reviews.models import Title, Genre, Category
from .serializers import (
                    TitleSerializer, CategorySerializer,
                    GenreSerializer, SignupSerializer, 
                    CustomUsersSerializer, TokenSerializer
    )
from .permission import IsAdmin


User = get_user_model()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


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
            user = get_object_or_404(User, email=email, confirmation_code=confirmation_code)
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
    queryset = User.objects.all()
    serializer_class = CustomUsersSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    search_fields = ('username',)

    @action(detail=False, permission_classes=(IsAuthenticated,),
            methods=['GET', 'PATCH'], url_path='me')
    def get_or_patch_me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user, many=False)
            return Response(serializer.data, status=HTTP_200_OK)
        serializer = self.get_serializer(
            instance=request.user,
            data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=HTTP_200_OK)
>>>>>>> c8090dd55aab208a1e0ef760ca2302fc289b218c
