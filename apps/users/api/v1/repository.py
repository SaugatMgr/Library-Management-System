from apps.users.models import CustomUser


class UserRepository:
    def get_all():
        return CustomUser.objects.filter()
