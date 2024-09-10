from rest_framework import serializers

from apps.membership.models import MembershipPlan


class MembershipPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipPlan
        fields = ("id", "name", "plan_type", "price", "duration_in_days")
        read_only_fields = ("id",)
