from rest_framework import mixins, viewsets, filters

from .models import Categories
from .serializers import (CategoriesSerializer)
from .permissions import IsAdminOrReadOnly

class CreateListViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet,):
    pass

class CategoriesViewSet(CreateListViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]
