from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.viewsets import CreateListViewSet
from users.models import User
from users.permissions import IsAdmin, IsAdminOrReadOnly, IsModerator
from users.serializers import UserSerializer

from api.models import Review, Title, User, Category, Comment, Genre
from api.permissions import IsOwnerOrReadOnly, ReadOnly, IsOwner
from api.serializers import (CommentsSerializer,
                             ReviewSerializer, TitleSerializer, GenreSerializer, CategorySerializer)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin | IsAdminUser,)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @me.mapping.patch
    def patch_me(self, request, **kwargs):
        user = request.user
        serializer = self.serializer_class(
            user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdmin | ReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ('category', 'year')  # 'genre'
    search_fields = ('name',)
    pagination_class = PageNumberPagination


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminUser | IsAdmin | IsModerator | IsOwner | ReadOnly,)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['id'])
        serializer.save(author=self.request.user, title_id=title)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['id'])
        return title.reviews.all()


class CategoriesViewSet(CreateListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser | IsAdmin | ReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUser | IsAdmin | ReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CommentsViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
