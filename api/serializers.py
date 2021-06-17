from django.db.models import Avg
from rest_framework import serializers

from api.models import Review, Title


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )

    def get_rating(self, title):
        return title.reviews.aggregate(rating=Avg('score'))['rating']


class ReviewSerilizer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Review
