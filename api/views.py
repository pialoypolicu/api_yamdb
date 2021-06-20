from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.filters import TitleFilter
from api.viewsets import CreateListViewSet
from users.models import User
from users.permissions import IsAdmin, IsAdminOrReadOnly, IsModerator
from users.serializers import UserSerializer

from api.models import Review, Title, User, Category, Comment, Genre, GenreTitle
from api.permissions import IsOwnerOrReadOnly, ReadOnly, IsOwner, MethodPermission, ObjectPermissions
from api.serializers import (CommentsSerializer,
                             ReviewSerializer, TitleSerializer, GenreSerializer, CategorySerializer,
                             TitleUnsafeSerializer)


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
    filter_backends = (
        filters.OrderingFilter,
        DjangoFilterBackend,
    )
    ordering_fields = ('id',)
    filterset_class = TitleFilter

    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleSerializer
        return TitleUnsafeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        safe_serializer = TitleSerializer(obj)
        return Response(safe_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        safe_serializer = TitleSerializer(obj)
        return Response(safe_serializer.data)

    def perform_update(self, serializer):
        return serializer.save()


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permissions = {
        'create': (IsAuthenticated,),
        'retrieve': (AllowAny,),
        'update': (ObjectPermissions,),
        'partial_update': (ObjectPermissions,),
        'destroy': (ObjectPermissions,),
        'list': (AllowAny,),
    }

    def get_permissions(self):
        permission_classes = self.permissions[self.action]
        return [permission() for permission in permission_classes]

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
    permissions = {
        'create': (IsAuthenticated,),
        'retrieve': (AllowAny,),
        'update': (ObjectPermissions,),
        'partial_update': (ObjectPermissions,),
        'destroy': (ObjectPermissions,),
        'list': (AllowAny,),
    }

    def get_permissions(self):
        permission_classes = self.permissions[self.action]
        return [permission() for permission in permission_classes]
