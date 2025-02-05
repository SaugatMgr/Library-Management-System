from rest_framework import serializers

from apps.users.models import CustomUser, CustomUserGroup, UserProfile


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserGroup
        fields = ("id", "name")


class UserListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="get_full_name")
    groups = UserGroupSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "name",
            "email",
            "groups",
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="get_full_name")
    groups = UserGroupSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "middle_name",
            "last_name",
            "name",
            "email",
            "groups",
        ]


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
