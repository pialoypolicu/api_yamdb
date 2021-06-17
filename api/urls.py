from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from api.views import ReviewViewSet, TitleViewSet, UserViewSet
from users.views import ObtainConfirmationCode, TokenObtainView

router_yamdb_v1 = DefaultRouter()
router_yamdb_v1.register('users', UserViewSet, basename='users')
router_yamdb_v1.register('titles', TitleViewSet, basename='titles_view')
router_yamdb_v1.register(r'titles/(?P<id>[^/.]+)/review', ReviewViewSet)

urlpatterns = [
    re_path(r'^(?P<version>v1)/', include(router_yamdb_v1.urls)),
    re_path(r'^(?P<version>v1)/token/', TokenObtainView.as_view()),
    re_path(r'^(?P<version>v1)/email/', ObtainConfirmationCode.as_view()),
]
