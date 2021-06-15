from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from api.models import Title, Review
from api.serializers import TitleSerializer, ReviewSerilizer


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'year', 'name']  # 'genre'
    search_fields = ['name', ]
    pagination_class = PageNumberPagination


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerilizer

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['id'])
        serializer.save(author=self.request.user, title=title)
