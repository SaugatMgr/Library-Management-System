import pyotp
import re
import random

from rest_framework import serializers

from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from apps.users.models import UserProfile, OTP
from utils.helpers import get_instance_by_attr


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


def validate_otp(otp):
    otp_regex = r"^\d+$"
    if not re.match(otp_regex, otp):
        raise serializers.ValidationError("OTP must be digits only.")


def validate_ph_no(phone_number):
    if not re.match(r"^\d{10}$", phone_number):
        raise serializers.ValidationError({"error": "Phone number must be 10 digits."})


def verify_otp(user, otp):
    otp_instance = get_instance_by_attr(OTP, "user", user)
    valid_otp = pyotp.TOTP(otp_instance.secret_key, interval=120)
    return valid_otp.verify(otp)
