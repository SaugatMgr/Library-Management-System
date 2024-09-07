from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAcceptable
from django_celery_beat.models import PeriodicTask, CrontabSchedule

from django.db import transaction

from apps.users.api.v1.helpers import verify_otp
from apps.users.api.v1.repository import UserProfileRepository, UserRepository
from apps.users.api.v1.serializers.post import (
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
    UserEmailVerificationSerializer,
    UserRegisterSerializer,
)
from apps.users.models import OTP, CustomUser
from apps.users.tasks import send_mail_to_user
from utils.helpers import get_instance_by_attr, send_otp_to_email


class UserAuthView(APIView):
    permission_classes = [IsAuthenticated]


class UserRegisterView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        data = request.data
        user_data = data.get("user_data")
        user_profile_data = data.get("user_profile_data")

        with transaction.atomic():
            user_register_serializer = UserRegisterSerializer(data=user_data)
            user_register_serializer.is_valid(raise_exception=True)
            user_validated_data = user_register_serializer.validated_data
            user_validated_data["is_active"] = False

            user = CustomUser.objects.create_user(**user_validated_data)
            user_profile_data["user"] = user.id
            UserProfileRepository.create_profile(user_profile_data)

            email = user.email
            otp = OTP.generate_otp(user=user)
            send_otp_to_email(email, otp)
            return Response(
                {
                    "message": f"An OTP has been sent to {email}. Please verify your email."
                }
            )


class UserEmailVerificationView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        data = request.data
        verify_email_serializer = UserEmailVerificationSerializer(data=data)
        verify_email_serializer.is_valid(raise_exception=True)
        validated_data = verify_email_serializer.validated_data

        email = request.query_params.get("email")
        user = get_instance_by_attr(CustomUser, "email", email)

        if verify_otp(user, validated_data["otp"]):
            user.is_active = True
            user.save()
            return Response({"message": "User verified successfully."})
        else:
            raise NotAcceptable({"error": "OTP is either invalid or expired."})


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


@api_view(["POST"])
def send_mail_celery(request):
    send_mail_to_user.delay()
    return Response({"message": "Mail sent successfully."})


@api_view(["POST"])
def schedule_mail_celery(request):
    data = request.data
    crontab, created = CrontabSchedule.objects.get_or_create(hour=11, minute=31)
    PeriodicTask.objects.create(
        name="send-email-every-day-at-11:31-PM",
        task="apps.users.tasks.send_mail_to_user",
        crontab=crontab,
        args=[data["subject"], data["message"]],
    )

    return Response({"message": "Mail scheduled successfully."})
