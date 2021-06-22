from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api import serializers
from api.filters import TitleFilter
from api.models import Category, Comment, Genre, Review, Title
from api.permissions import ObjectPatchDeletePermission, ReadOnly
from api.viewsets import CreateListViewSet
from users.models import User
from users.permissions import IsAdmin
from users.serializers import UserSerializer


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
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = serializers.TitleListRetrieveSerializer
    permission_classes = (IsAdmin | IsAdminUser | ReadOnly,)
    filterset_class = TitleFilter

    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return serializers.TitleListRetrieveSerializer
        return serializers.TitlePostPatchSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        safe_serializer = serializers.TitleListRetrieveSerializer(obj)
        return Response(
            safe_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        return serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)
        obj = self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        safe_serializer = serializers.TitleListRetrieveSerializer(obj)
        return Response(safe_serializer.data)

    def perform_update(self, serializer):
        return serializer.save()


class ReviewViewSet(ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permissions = {
        'create': (IsAuthenticated,),
        'retrieve': (AllowAny,),
        'update': (ObjectPatchDeletePermission,),
        'partial_update': (ObjectPatchDeletePermission,),
        'destroy': (ObjectPatchDeletePermission,),
        'list': (AllowAny,),
    }

    def get_permissions(self):
        permission_classes = self.permissions[self.action]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()


class CategoriesViewSet(CreateListViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (IsAdminUser | IsAdmin | ReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = (IsAdminUser | IsAdmin | ReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CommentsViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentsSerializer
    permissions = {
        'create': (IsAuthenticated,),
        'retrieve': (AllowAny,),
        'update': (ObjectPatchDeletePermission,),
        'partial_update': (ObjectPatchDeletePermission,),
        'destroy': (ObjectPatchDeletePermission,),
        'list': (AllowAny,),
    }

    def get_permissions(self):
        permission_classes = self.permissions[self.action]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review.comments.all()
