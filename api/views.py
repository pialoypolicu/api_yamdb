from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from users.models import User
from users.permissions import IsAdmin, IsAdminOrReadOnly
from users.serializers import UserSerializer

from api.models import Categories, Review, Title, User
from api.permissions import IsOwnerOrReadOnly
from api.serializers import (CategoriesSerializer, ReviewSerilizer,
                             TitleSerializer)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin, IsAdminUser)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @me.mapping.patch
    def patch_me(self, request):
        user = request.user
        if user.role != User.Roles.ADMIN:
            request.data.pop('role', None)
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
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'year']  # 'genre'
    search_fields = ['name', ]
    pagination_class = PageNumberPagination


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerilizer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['id'])
        serializer.save(author=self.request.user, title_id=title)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['id'])
        return title.reviews.all()


class CreateListViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet, ):
    pass


class CategoriesViewSet(CreateListViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
