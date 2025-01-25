from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.books.api.v1.serializers.get import UserNotificationSerializer
from apps.users.api.v1.repository import UserProfileRepository, UserRepository
from apps.users.api.v1.serializers.get import (
    UserDetailSerializer,
    UserListSerializer,
    UserProfileDetailSerializer,
    UserProfileListSerializer,
)
from apps.users.api.v1.serializers.post import UserProfileCreateUpdateSerializer
from apps.books.models import Notification
from utils.pagination import CustomPageSizePagination
from utils.permissions import (
    AdminPermission,
    ProfileOwnerOrAdminPermission,
    SelfOrAdminPermission,
)


class UserViewset(ModelViewSet):
    serializer_action = {
        "list": UserListSerializer,
        "retrieve": UserDetailSerializer,
        "create": UserListSerializer,
        "update": UserListSerializer,
        "get_notifications": UserNotificationSerializer,
    }
    action_permissions = {
        "create": [AdminPermission],
        "list": [AdminPermission],
        "retrieve": [SelfOrAdminPermission],
        "update": [AdminPermission],
        "destroy": [AdminPermission],
        "change_user_password": [AdminPermission],
    }
    pagination_class = CustomPageSizePagination

    def get_queryset(self):
        return UserRepository.get_all()

    def get_permissions(self):
        return [
            permission()
            for permission in self.action_permissions.get(
                self.action, [AdminPermission]
            )
        ]

    def get_serializer_class(self):
        return self.serializer_action.get(self.action)

    @action(detail=True, methods=["post"], url_path="change-password")
    def change_user_password(self, request, pk=None):
        user = self.get_object()
        UserRepository.change_user_password(user, request.data)
        return Response({"message": "Password changed successfully."})

    @action(detail=True, methods=["get"], url_path="notifications")
    def get_notifications(self, request, pk=None):
        current_user = self.get_object()
        user_notifications = Notification.objects.filter(user=current_user)
        paginator = CustomPageSizePagination()
        paginated_user_notifications = paginator.paginate_queryset(
            user_notifications, request
        )
        serializer = self.get_serializer(paginated_user_notifications, many=True)
        return paginator.get_paginated_response(serializer.data)


class UserProfileViewSet(ModelViewSet):
    serializer_action = {
        "list": UserProfileListSerializer,
        "retrieve": UserProfileDetailSerializer,
        "update": UserProfileCreateUpdateSerializer,
    }
    pagination_class = CustomPageSizePagination
    permission_classes = [ProfileOwnerOrAdminPermission]

    def get_queryset(self):
        return UserProfileRepository.get_all(user=self.request.user)

    def get_serializer_class(self):
        return self.serializer_action.get(self.action)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        UserProfileRepository.update_profile(instance, data)
        return Response({"message": "User Profile updated successfully."})
