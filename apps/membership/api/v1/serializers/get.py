from rest_framework import serializers

from apps.membership.api.v1.serializers.general import MembershipPlanSerializer
from apps.membership.models import Membership
from apps.users.api.v1.serializers.get import UserDetailSerializer


class MembershipListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ("id", "user", "plan", "start_date", "end_date")


class MembershipDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    plan = MembershipPlanSerializer()

    class Meta:
        model = Membership
        fields = ("id", "user", "plan", "start_date", "end_date")
