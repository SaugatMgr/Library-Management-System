from rest_framework import serializers

from apps.users.models import CustomUser, CustomUserGroup, UserProfile


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


class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "id",
            "user",
            "library_card_number",
            "address",
            "phone_number",
            "date_of_birth",
            "gender",
            "profile_picture",
            "bio",
        )


class UserProfileDetailSerializer(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "user",
            "library_card_number",
            "address",
            "phone_number",
            "date_of_birth",
            "gender",
            "profile_picture",
            "bio",
        )
