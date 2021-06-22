from rest_framework import serializers

from users.models import User
from users.roles import Roles


class TokenObtainSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField()


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role',
        )

    def update(self, user, validated_data):
        request = self.context.get('request')
        if request:
            request_user = request.user
            if (request_user.role != Roles.ADMIN
                    or not request_user.is_superuser
                    or not request_user.is_staff):
                validated_data.pop('role', None)
        user = super().update(user, validated_data)
        return user
