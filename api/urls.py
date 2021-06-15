from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import TitleViewSet, ReviewViewSet

router_yamdb_v1 = DefaultRouter()
router_yamdb_v1.register('titles', TitleViewSet, basename='titles_view')
router_yamdb_v1.register(r'titles/(?P<id>[^/.]+)/review', ReviewViewSet)

urlpatterns = [
    path('v1/', include(router_yamdb_v1.urls))
]
