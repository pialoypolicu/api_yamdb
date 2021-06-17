from django.db.models import Avg
from rest_framework import serializers

from api.models import Review, Title, User


class UserSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(source='description')

    class Meta:
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role',
        )
        model = User


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
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        user = self.context['request'].user
        review = self.context['view'].kwargs['id']
        if Review.objects.filter(title_id_id=review).filter(author=user):
            raise serializers.ValidationError('Вы уже оставили отзыв.')
        return data
