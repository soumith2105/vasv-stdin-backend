from rest_framework import permissions


class IsOwnerOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.semester.student == request.user
