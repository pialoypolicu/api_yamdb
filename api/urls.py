from django.urls import include, re_path
from rest_framework.routers import DefaultRouter
from users.views import ObtainConfirmationCode, TokenObtainView

from api.views import (CategoriesViewSet, CommentsViewSet, ReviewViewSet,
                       TitleViewSet, UserViewSet, GenreViewSet)

router_yamdb_v1 = DefaultRouter()
router_yamdb_v1.register(
    'users',
    UserViewSet,
    basename='users')
router_yamdb_v1.register(
    'titles',
    TitleViewSet,
    basename='titles')
router_yamdb_v1.register(
    r'titles/(?P<id>[^/.]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_yamdb_v1.register(
    r'titles/(?P<id1>[^/.]+)/reviews/(?P<id2>[^/.]+)/comments',
    CommentsViewSet,
    basename='comments'
)
router_yamdb_v1.register(
    'categories',
    CategoriesViewSet,
    basename='categories'
)
router_yamdb_v1.register(
    'genres',
    GenreViewSet,
    basename='genres'
)

urlpatterns = [
    re_path(r'^(?P<version>v1)/', include(router_yamdb_v1.urls)),
    re_path(r'^(?P<version>v1)/token/', TokenObtainView.as_view()),
    re_path(r'^(?P<version>v1)/email/', ObtainConfirmationCode.as_view()),
]
