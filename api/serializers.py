from rest_framework import serializers


from api.models import Title, Review


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerilizer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Review
