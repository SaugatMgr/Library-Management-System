from rest_framework import permissions
from utils.constants import UserGroupChoices
from utils.helpers import generate_error


class AdminPermission(permissions.BasePermission):
    message = generate_error(message="Only Admin can access.", code="admin_only")

    def has_permission(self, request, view):
        user_group = request.user.groups.all().values_list("name", flat=True)
        is_user_admin = UserGroupChoices.ADMIN in user_group
        return (
            request.user
            and request.user.is_active
            and (request.user.is_superuser or is_user_admin)
        )


class SelfOrAdminPermission(permissions.BasePermission):
    message = generate_error(
        message="Only Self or Admin can access.", code="self_or_admin_only"
    )

    def has_object_permission(self, request, view, obj):
        user = request.user
        user_group = user.groups.all().values_list("name", flat=True)
        is_user_admin = UserGroupChoices.ADMIN in user_group
        if user:
            return user.is_active and (
                user.is_superuser or obj == request.user or is_user_admin
            )


class LibrarianOrAdminPermission(permissions.BasePermission):
    message = generate_error(
        message="Only Librarian or Admin can access.", code="librarian_or_admin_only"
    )

    def has_permission(self, request, view):
        user = request.user
        user_group = user.groups.all().values_list("name", flat=True)
        is_user_admin = UserGroupChoices.ADMIN in user_group
        is_user_librarian = UserGroupChoices.LIBRARIAN in user_group
        if user:
            return user.is_active and (
                is_user_admin or is_user_librarian or user.is_superuser
            )


class ProfileOwnerOrAdminPermission(permissions.BasePermission):
    message = generate_error(
        message="Only Profile Owner or Admin can access.", code="owner_or_admin_only"
    )

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user:
            return (
                user.is_active
                and user.is_authenticated
                and (user.is_superuser or obj.user == request.user)
            )


class NotificationUserOrLibrarianOrAdminPermission(permissions.BasePermission):
    message = generate_error(
        message="Only Notification Owner or Librarian or Admin can access.",
        code="owner_or_librarian_or_admin_only",
    )

    def has_object_permission(self, request, view, obj):
        user = request.user
        user_group = user.groups.all().values_list("name", flat=True)
        is_user_admin = UserGroupChoices.ADMIN in user_group
        is_user_librarian = UserGroupChoices.LIBRARIAN in user_group
        if user:
            return (
                user.is_active
                and user.is_authenticated
                and (
                    user.is_superuser
                    or obj.user == request.user
                    or is_user_admin
                    or is_user_librarian
                )
            )
