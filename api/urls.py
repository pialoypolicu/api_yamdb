from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from api import views
from users.views import ObtainConfirmationCode, TokenObtainView

router_yamdb_v1 = DefaultRouter()
router_yamdb_v1.register(
    'users',
    views.UserViewSet,
    basename='users')
router_yamdb_v1.register(
    'titles',
    views.TitleViewSet,
    basename='titles')
router_yamdb_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
router_yamdb_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentsViewSet,
    basename='comments'
)
router_yamdb_v1.register(
    'categories',
    views.CategoriesViewSet,
    basename='categories'
)
router_yamdb_v1.register(
    'genres',
    views.GenreViewSet,
    basename='genres'
)

urlpatterns = [
    re_path(r'^(?P<version>v1)/', include(router_yamdb_v1.urls)),
    re_path(r'^(?P<version>v1)/token/', TokenObtainView.as_view()),
    re_path(r'^(?P<version>v1)/email/', ObtainConfirmationCode.as_view()),
]
