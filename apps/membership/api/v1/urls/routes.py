from rest_framework.routers import DefaultRouter

from apps.membership.api.v1.views.viewsets import (
    MemberShipModelViewSet,
    MemberShipPlanModelViewSet,
)

membership_router = DefaultRouter()

membership_router.register("membership", MemberShipModelViewSet, basename="membership")
membership_router.register(
    "membership-plans", MemberShipPlanModelViewSet, basename="membership-plans"
)
