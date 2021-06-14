from rest_framework.routers import DefaultRouter
from django.urls import path, include
from api.views import TitlesViewSet

router_yamdb_v1 = DefaultRouter()
router_yamdb_v1.register('titles', TitlesViewSet, basename='titles_view')

urlpatterns = [
    path('v1', include(router_yamdb_v1.urls))
]