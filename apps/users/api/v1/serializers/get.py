from rest_framework import serializers

from apps.users.models import CustomUser


class UserListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="get_full_name")

    class Meta:
        model = CustomUser
        fields = ("id", "name", "email", "groups")
