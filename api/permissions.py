from rest_framework import permissions

from api.models import User


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.Roles.ADMIN


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.Roles.MODERATOR


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.method in permissions.SAFE_METHODS)
