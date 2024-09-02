from typing import List

from django.db import transaction
from django.db.models.query import QuerySet

from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, BasePermission

from apps.digital_resources.api.v1.repository import DigitalResourcesRepository
from apps.digital_resources.api.v1.serializers.get import (
    DigitalResourceListDetailSerializer,
)
from apps.digital_resources.api.v1.serializers.post import (
    DigitalResourceCreateUpdateSerializer,
)
from apps.digital_resources.models import DigitalResource

from utils.helpers import to_internal_value
from utils.permissions import (
    LibrarianOrAdminPermission,
)


class DigitalResourceModelViewSet(ModelViewSet):
    serializer_action = {
        "list": DigitalResourceListDetailSerializer,
        "retrieve": DigitalResourceListDetailSerializer,
        "create": DigitalResourceCreateUpdateSerializer,
        "update": DigitalResourceCreateUpdateSerializer,
    }
    action_permissions = {
        "create": [LibrarianOrAdminPermission],
        "list": [AllowAny],
        "retrieve": [AllowAny],
        "update": [LibrarianOrAdminPermission],
        "destroy": [LibrarianOrAdminPermission],
    }

    def get_queryset(self) -> QuerySet:
        return DigitalResourcesRepository.get_all()

    def get_serializer_class(self) -> type[Serializer] | None:
        return self.serializer_action.get(self.action)

    def get_permissions(self) -> List[BasePermission]:
        return [
            permission()
            for permission in self.action_permissions.get(
                self.action, [LibrarianOrAdminPermission]
            )
        ]

    def create(self, request, *args, **kwargs) -> Response:
        with transaction.atomic():
            data = request.data
            data["file"] = to_internal_value(data.get("file"))
            digital_res_serializer = self.get_serializer(data=request.data)
            digital_res_serializer.is_valid(raise_exception=True)
            digital_res_serializer.save()
            return Response(
                {"message": "Digital Resource added successfully."}, status=201
            )

    def update(self, request, *args, **kwargs) -> Response:
        with transaction.atomic():
            data = request.data
            data["file"] = to_internal_value(data.get("file"))
            digital_res_serializer = self.get_serializer(
                instance=self.get_object(), data=request.data, partial=True
            )
            digital_res_serializer.is_valid(raise_exception=True)
            digital_res_serializer.save()
            return Response(
                {"message": "Digital Resource updated successfully."}, status=200
            )
