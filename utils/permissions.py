from rest_framework import permissions
from utils.constants import UserGroupChoices


class AdminPermission(permissions.BasePermission):
    message = "Only Admin can access."

    def has_permission(self, request, view):
        user = request.user

        if user:
            return user.is_superuser


class LibraryAdminPermission(permissions.BasePermission):
    message = "Only Library Admin can access."

    def has_permission(self, request, view):
        user = request.user
        if user:
            return user.is_active and (
                UserGroupChoices.ADMIN
                in user.groups.all().values_list("name", flat=True)
            )


class ProfileOwnerOrAdminPermission(permissions.BasePermission):
    message = "Only the profile user or Admin can access"

    def has_permission(self, request, view):
        user = request.user
        if user:
            if request.method in ["GET", "PUT"]:
                return user.is_active and user.is_authenticated
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user:
            return (
                user.is_active
                and user.is_authenticated
                and (user.is_superuser or obj.user == request.user)
            )
