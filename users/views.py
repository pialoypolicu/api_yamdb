from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from users import serializers
from users.models import User
from users.permissions import UnauthorizedOnly
from users.utils import (get_confirmation_code, get_token_for_user,
                         get_username_from_email, send_confirmation_code)


class TokenObtainView(APIView):
    permission_classes = (UnauthorizedOnly,)

    def post(self, request, **kwargs):
        serializer = serializers.TokenObtainSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(User, email=serializer.data['email'])
            if user.check_confirmation_code(
                    serializer.data['confirmation_code']
            ):
                token = get_token_for_user(user)
                return Response(token)


class ObtainConfirmationCode(APIView):
    permission_classes = (UnauthorizedOnly,)

    def post(self, request, **kwargs):
        serializer = serializers.EmailSerializer(
            data=request.data
        )
        if serializer.is_valid(raise_exception=True):
            user, created = User.objects.get_or_create(
                email=serializer.data['email']
            )
            confirmation_code = get_confirmation_code()
            user.set_confirmation_code(confirmation_code)
            send_confirmation_code(user, confirmation_code)
            if created:
                user.username = get_username_from_email(
                    serializer.data['email']
                )
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
