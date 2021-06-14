from rest_framework.viewsets import ModelViewSet

from api.models import Title
from api.serializers import TitleSerializer


class TitlesViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
