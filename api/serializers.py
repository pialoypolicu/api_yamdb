from django.db.models import Avg
from rest_framework import serializers

from api.models import Review, Title, Genre, Category, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    category = CategorySerializer(required=False)
    genre = GenreSerializer(required=False, many=True)

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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        user = self.context['request'].user
        review = self.context['view'].kwargs['id']
        if self.context.get('request').method == 'POST' and (
                Review.objects.filter(title_id_id=review).filter(author=user)
        ):
            raise serializers.ValidationError('Вы уже оставили отзыв.')
        return data


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
