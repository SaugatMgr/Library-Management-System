from rest_framework import permissions
from utils.constants import UserGroupChoices
from utils.helpers import generate_error


class AdminPermission(permissions.BasePermission):
    message = generate_error(message="Only Admin can access.", code="admin_only")

    def has_permission(self, request, view):
        return request.user and request.user.is_active and request.user.is_superuser


class LibrarianOrAdminPermission(permissions.BasePermission):
    message = generate_error(
        message="Only Librarian or Admin can access.", code="librarian_or_admin_only"
    )

    def has_permission(self, request, view):
        user = request.user
        if user:
            return user.is_active and (
                UserGroupChoices.ADMIN
                in user.groups.all().values_list("name", flat=True)
                or user.is_superuser
            )


class ProfileOwnerOrAdminPermission(permissions.BasePermission):
    message = generate_error(
        message="Only Profile Owner or Admin can access.", code="owner_or_admin_only"
    )

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
