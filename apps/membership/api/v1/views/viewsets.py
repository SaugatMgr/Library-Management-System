from rest_framework.viewsets import ModelViewSet

from apps.membership.api.v1.serializers.general import (
    MembershipPlanSerializer,
)
from apps.membership.api.v1.serializers.get import (
    MembershipDetailSerializer,
    MembershipListSerializer,
)
from apps.membership.api.v1.serializers.post import MembershipCreateUpdateSerializer
from apps.membership.models import Membership, MembershipPlan
from utils.pagination import CustomPageSizePagination


class MemberShipModelViewSet(ModelViewSet):
    queryset = Membership.objects.all()
    serializer_action = {
        "list": MembershipListSerializer,
        "retrieve": MembershipDetailSerializer,
        "create": MembershipCreateUpdateSerializer,
        "update": MembershipCreateUpdateSerializer,
    }
    pagination_class = CustomPageSizePagination

    def get_serializer_class(self):
        return self.serializer_action.get(self.action)


class MemberShipPlanModelViewSet(ModelViewSet):
    queryset = MembershipPlan.objects.all()
    serializer_class = MembershipPlanSerializer
    pagination_class = CustomPageSizePagination
