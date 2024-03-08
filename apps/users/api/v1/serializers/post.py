import re
from typing import Any, Dict

from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenVerifySerializer,
)
from rest_framework_simplejwt.settings import api_settings

from apps.users.models import CustomUser, UserProfile


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "password",
        )
        write_only_fields = "password"


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        data["user"] = self.user
        data["access_expires_on"] = api_settings.ACCESS_TOKEN_LIFETIME
        data["refresh_expires_on"] = api_settings.REFRESH_TOKEN_LIFETIME

        return data


class CustomTokenVerifySerializer(TokenVerifySerializer):
    token = serializers.CharField(max_length=500, required=True)


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "user",
            "address",
            "phone_number",
            "date_of_birth",
            "gender",
            "profile_picture",
            "bio",
        )

    def validate_phone_number(self, value):
        if not re.match(r"^\d{10}$", value):
            raise serializers.ValidationError(
                {"error": "Phone number must be 10 digits."}
            )
        return value
