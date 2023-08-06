from rest_framework import permissions


class UserAPIPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.is_superuser
        elif request.method == 'POST':
            return True


class UserDetailAPIPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(request.method)
        if request.method == 'GET':
            return obj == request.user
        elif request.method == 'PUT':
            return obj == request.user
        return True


class UserProfileDetailAPIPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return obj == request.user
        elif request.method == 'PUT':
            return obj == request.user
        elif request.method == 'DELETE':
            return obj == request.user
        return True


class SymbolAPIPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_superuser
        return True
