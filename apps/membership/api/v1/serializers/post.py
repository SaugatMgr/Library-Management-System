from rest_framework import serializers

from apps.membership.models import Membership


class MembershipCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ("user", "plan")
