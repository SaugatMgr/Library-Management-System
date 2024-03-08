from apps.users.api.v1.serializers.post import UserProfileUpdateSerializer
from apps.users.models import CustomUser, UserProfile
from utils.helpers import to_internal_value


class UserRepository:
    @classmethod
    def get_all(cls):
        return CustomUser.objects.filter()


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
