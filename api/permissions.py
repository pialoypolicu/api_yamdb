from rest_framework import permissions

from users.models import User


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.method in permissions.SAFE_METHODS)


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user.username


class ObjectPatchDeletePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        roles_with_permissions = (
            User.Roles.MODERATOR,
            User.Roles.ADMIN,
        )
        return (request.user.role in roles_with_permissions
                or obj.author == request.user)
