from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.users.api.v1.repository import UserRepository

from apps.users.api.v1.serializers.post import (
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
    UserRegisterSerializer,
)
from apps.users.models import OTP, CustomUser
from utils.helpers import get_instance_by_attr, send_otp_to_email


class UserAuthView(APIView):
    permission_classes = [IsAuthenticated]


class UserRegisterView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        user_register_serializer = UserRegisterSerializer(data=request.data)
        user_register_serializer.is_valid(raise_exception=True)
        validated_data = user_register_serializer.validated_data
        CustomUser.objects.create_user(**validated_data)
        return Response({"message": "User Registered Successfully."})


class PasswordResetRequestView(APIView):
    def post(self, request, *args, **kwargs):
        pwd_reset_req_serializer = PasswordResetRequestSerializer(data=request.data)
        pwd_reset_req_serializer.is_valid(raise_exception=True)
        email = pwd_reset_req_serializer.validated_data["email"]
        user = get_instance_by_attr(CustomUser, "email", email)
        otp = OTP.generate_otp(user=user)

        send_otp_to_email(user.email, otp)

        return Response({"message": "OTP sent to email successfully."})


class ResetPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        pwd_reset_serializer = PasswordResetSerializer(
            data=request.data, context={"user": user}
        )
        pwd_reset_serializer.is_valid(raise_exception=True)
        validated_data = pwd_reset_serializer.validated_data
        result = UserRepository.reset_password(user, validated_data)
        return Response(result)


class ChangePasswordView(UserAuthView):
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            change_pwd_serializer = ChangePasswordSerializer(
                data=request.data, context={"user": request.user}
            )
            change_pwd_serializer.is_valid(raise_exception=True)
            new_password = change_pwd_serializer.validated_data["new_password"]

            user.set_password(new_password)
            user.save()
            return Response({"message": "Password Changed successfully."})
        return Response({"error": "UnAuthorized"}, status=status.HTTP_401_UNAUTHORIZED)
