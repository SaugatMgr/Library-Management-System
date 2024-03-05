from rest_framework import serializers

from apps.users.models import CustomUser, CustomUserGroup


class UserListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="get_full_name")

    class Meta:
        model = CustomUser
        fields = ("id", "name", "email", "groups")


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserGroup
        fields = ("id", "name")


class UserDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="get_full_name")
    groups = UserGroupSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ("id", "name", "email", "groups")
