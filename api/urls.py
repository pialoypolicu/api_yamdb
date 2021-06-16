from rest_framework import routers
from .views import CategoriesViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register('categories', CategoriesViewSet, basename='api_categories')
urlpatterns = [
    path('v1/', include(router.urls)),
]
