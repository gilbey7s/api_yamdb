import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.validators import ValidationError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_403_FORBIDDEN)
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Comment, Genre, Review, Title

from .filters import TitleFilter
from .pagination import CommentsPagination, ReviewsPagination, TitlesPagination
from .permissions import (IsAdmin, IsAdminOrReadOnly, ReadOnlyPermission,
                          ReviewCommentPermission)
from .serializers import (CategorySerializer, CommentSerializer,
                          CustomUsersSerializer, GenreSerializer,
                          ReviewCreateSerializer, ReviewSerializer,
                          SignupSerializer, TitleReadSerializer,
                          TitleSerializer, TitleWriteSerializer,
                          TokenSerializer)

User = get_user_model()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = ReviewCommentPermission
    pagination_class = ReviewsPagination

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        return Review.objects.filter(title=title)


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
                  [email, ],
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
            user = get_object_or_404(
                User, email=email, confirmation_code=confirmation_code)
            if user:
                try:
                    token = RefreshToken.for_user(user).access_token
                    return Response({'token': str(token)},
                                    status=HTTP_201_CREATED)
                except Exception as error:
                    raise error
            else:
                result = {
                    'error': 'Can not authenticate with the given credentials'}
                return Response(result, status=HTTP_403_FORBIDDEN)
        except KeyError:
            result = {
                'error': 'Please provide a email and a confirmation code'}
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


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score')
                                            ).order_by('-name')
    serializer_class = TitleSerializer
    permission_classes = (ReadOnlyPermission | IsAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'category',
        'genre',
        'name',
        'year',
    )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return TitleReadSerializer
        return TitleWriteSerializer


class Genres(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = TitlesPagination


class GenreDetail(generics.DestroyAPIView):
    serializer_class = GenreSerializer
    permission_classes = (IsAdmin,)

    def get_object(self):
        return get_object_or_404(Genre, slug=self.kwargs.get('slug'))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class Categories(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdmin | ReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryDetail(generics.DestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = (IsAdmin,)

    def get_object(self):
        return get_object_or_404(Category, slug=self.kwargs.get('slug'))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (ReviewCommentPermission,)
    pagination_class = ReviewsPagination

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        if Review.objects.filter(
                author=self.request.user, title=title).exists():
            raise ValidationError("Вы уже оставляли отзыв на это произведение")
        serializer.save(author=self.request.user, title=title)

    def get_permissions(self):
        if self.action == 'update':
            raise MethodNotAllowed('PUT request is not allowed')
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewCreateSerializer
        return ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (ReviewCommentPermission,)
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
