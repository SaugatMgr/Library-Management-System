from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from apps.users.api.v1.repository import UserProfileRepository, UserRepository
from apps.users.api.v1.serializers.get import (
    UserDetailSerializer,
    UserListSerializer,
    UserProfileDetailSerializer,
    UserProfileListSerializer,
)
from apps.users.api.v1.serializers.post import UserProfileCreateUpdateSerializer
from utils.permissions import AdminPermission, ProfileOwnerOrAdminPermission


class UserViewset(ModelViewSet):
    permission_classes = [AdminPermission]
    serializer_action = {
        "list": UserListSerializer,
        "retrieve": UserDetailSerializer,
        "create": UserListSerializer,
        "update": UserListSerializer,
    }

    def get_queryset(self):
        return UserRepository.get_all()

    def get_serializer_class(self):
        return self.serializer_action.get(self.action)


class UserProfileViewSet(ModelViewSet):
    serializer_action = {
        "list": UserProfileListSerializer,
        "retrieve": UserProfileDetailSerializer,
        "update": UserProfileCreateUpdateSerializer,
    }
    http_method_names = ["get", "put"]
    permission_classes = [ProfileOwnerOrAdminPermission]

    def get_queryset(self):
        return UserProfileRepository.get_all()

    def get_serializer_class(self):
        return self.serializer_action.get(self.action)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        UserProfileRepository.update_profile(instance, data)
        return Response({"message": "User Profile updated successfully."})
