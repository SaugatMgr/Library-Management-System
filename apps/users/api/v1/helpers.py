import random

from rest_framework import serializers

from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from apps.users.models import UserProfile


def generate_lib_card_no():
    while True:
        library_card_no = settings.LIBRARY_CARD_NO_PREFIX + str(
            random.randint(10000000000000, 99999999999999)
        )
        if not UserProfile.objects.filter(library_card_number=library_card_no).exists():
            return library_card_no


def validate_password_fields(
    new_password, confirm_password, user=None, old_password=None
):
    if user and old_password:
        if not user.check_password(old_password):
            raise serializers.ValidationError(
                {"old_password": "Old password is incorrect."}
            )
    if new_password != confirm_password:
        raise serializers.ValidationError(
            {"password": "The two password fields do not match."}
        )
    try:
        validate_password(new_password, user)
    except DjangoValidationError as err:
        raise serializers.ValidationError({"error": err.messages})
