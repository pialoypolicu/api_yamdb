from rest_framework import permissions

from users.models import User


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.role == User.Roles.ADMIN
                or request.method in permissions.SAFE_METHODS)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.Roles.ADMIN


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.Roles.MODERATOR


class UnauthorizedOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated


class ReadOnlyAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                and (request.user.role == User.Roles.ADMIN
                     or request.user.is_superuser)
                )
