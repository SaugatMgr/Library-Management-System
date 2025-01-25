from apps.users.api.v1.helpers import generate_lib_card_no, verify_otp
from apps.users.api.v1.serializers.post import UserProfileCreateUpdateSerializer
from apps.users.models import CustomUser, UserProfile
from utils.helpers import to_internal_value


class UserRepository:
    @classmethod
    def get_all(cls):
        return CustomUser.objects.filter()

    @classmethod
    def reset_password(cls, user, data):
        otp = data["otp"]
        new_pwd = data["new_password"]

        if verify_otp(user, otp):
            user.set_password(new_pwd)
            user.save()
            return {"message": "Password reset successfully."}
        else:
            return {"error": "OTP is either invalid or expired."}

    @staticmethod
    def change_user_password(user, data):
        user.set_password(data["new_password"])
        user.save()


class UserProfileRepository:
    @classmethod
    def get_all(cls, user):
        if user.is_superuser:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=user)

    @classmethod
    def create_or_update_profile(cls, data, instance=None):
        if data.get("profile_picture"):
            data["profile_picture"] = to_internal_value(data["profile_picture"])
        if not instance:
            profile_serializer = UserProfileCreateUpdateSerializer(data=data)
            profile_serializer.is_valid(raise_exception=True)
            profile = profile_serializer.save()
            profile.library_card_number = generate_lib_card_no()
            profile.save()
            return
        profile_serializer = UserProfileCreateUpdateSerializer(
            instance=instance, data=data, partial=True
        )
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()

    @classmethod
    def create_profile(cls, data):
        cls.create_or_update_profile(data)

    @classmethod
    def update_profile(cls, instance, data):
        cls.create_or_update_profile(data, instance=instance)
