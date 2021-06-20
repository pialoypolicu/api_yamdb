from rest_framework import permissions


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user
                or request.method in permissions.SAFE_METHODS)


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class MethodPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'DELETE']:
            role_status = request.user.role in ['moderator', 'admin']
            return obj.author == request.user or role_status
        elif request.method == 'POST':
            return request.user.role == 'user'
        elif request.method == 'GET':
            return request.user.is_anonymous or (
                request.user.role in ['user', 'moderator', 'admin'])
        else:
            return False