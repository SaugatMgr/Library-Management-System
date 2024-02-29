from typing import Any

from django.core.management import BaseCommand

from apps.users.models import CustomUserGroup
from utils.constants import UserGroupChoices


class Command(BaseCommand):
    help = "This command is used to create user groups."

    def handle(self, *args: Any, **options: Any) -> str | None:
        for group in UserGroupChoices:
            CustomUserGroup.objects.create(name=group)
