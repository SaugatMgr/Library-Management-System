from rest_framework.viewsets import ModelViewSet

from apps.users.api.v1.repository import UserRepository
from apps.users.api.v1.serializers.get import UserListSerializer


class UserViewset(ModelViewSet):
    serializer_action = {
        "list": UserListSerializer,
        "retrieve": UserListSerializer,
        "create": UserListSerializer,
        "update": UserListSerializer,
    }

    def get_queryset(self):
        return UserRepository.get_all()

    def get_serializer_class(self):
        return self.serializer_action.get(self.action)
