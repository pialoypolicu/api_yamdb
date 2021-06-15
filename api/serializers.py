from rest_framework import serializers

from api.models import Title, User


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
    class Meta:
        fields = '__all__'
        model = Title
