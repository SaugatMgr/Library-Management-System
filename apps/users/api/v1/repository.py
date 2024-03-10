import pyotp

from apps.users.api.v1.serializers.post import UserProfileUpdateSerializer
from apps.users.models import CustomUser, UserProfile, OTP
from utils.helpers import get_instance_by_attr, to_internal_value


class UserRepository:
    @classmethod
    def get_all(cls):
        return CustomUser.objects.filter()

    @classmethod
    def reset_password(cls, user, data):
        otp = data["otp"]
        new_pwd = data["new_password"]

        otp_instance = get_instance_by_attr(OTP, "user", user)
        valid_otp = pyotp.TOTP(otp_instance.secret_key, interval=120)

        if valid_otp.verify(otp):
            user.set_password(new_pwd)
            user.save()
            return {"message": "Password reset successfully."}
        else:
            return {"error": "OTP is either invalid or expired."}


class UserProfileRepository:
    @classmethod
    def get_all(cls):
        return UserProfile.objects.filter()

    @classmethod
    def update_profile(cls, instance, data):
        if data.get("profile_picture"):
            data["profile_picture"] = to_internal_value(data["profile_picture"])
        profile_serializer = UserProfileUpdateSerializer(instance=instance, data=data)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()
