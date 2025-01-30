import uuid
import pyotp

from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.managers import CustomUserManager
from utils.constants import GenderChoices, UserGroupChoices
from utils.models import CommonInfo


class CustomUserGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        _("name"),
        choices=UserGroupChoices.choices,
        max_length=100,
    )
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("permissions"),
        related_name="permissions",
        blank=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = _("group")
        verbose_name_plural = _("groups")


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    middle_name = models.CharField(
        _("middle name"), max_length=64, blank=True, null=True
    )
    username = None
    email = models.EmailField(_("email address"), unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    groups = models.ManyToManyField(
        CustomUserGroup,
        help_text=_(
            "The group this user belongs to. The user will be able to perform "
            "all actions according to respective permissions."
        ),
        verbose_name=_("groups"),
        blank=True,
        related_name="users",
        related_query_name="user",
    )

    objects = CustomUserManager()

    class Meta:
        ordering = ["email"]

    @property
    def get_full_name(self) -> str:
        return (
            f"{self.first_name} {self.middle_name} {self.last_name}"
            if self.middle_name
            else f"{self.first_name} {self.last_name}"
        )

    def __str__(self) -> str:
        return self.email


class UserProfile(CommonInfo):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to="user/profile/",
        blank=True,
        null=True,
        verbose_name=_("Profile Picture"),
    )
    library_card_number = models.CharField(
        max_length=50, unique=True, verbose_name=_("Library Card No.")
    )
    address = models.CharField(max_length=255, blank=True, verbose_name=_("Address"))
    phone_number = models.CharField(
        max_length=10, unique=True, blank=True, null=True, verbose_name=_("Phone No.")
    )
    date_of_birth = models.DateField(
        blank=True, null=True, verbose_name=_("Date of Birth")
    )
    gender = models.CharField(
        max_length=1,
        choices=GenderChoices.choices,
        blank=True,
        verbose_name=_("Gender"),
    )
    bio = models.TextField(blank=True, verbose_name=_("Bio"))

    def __str__(self) -> str:
        return f"{self.user.get_full_name} Profile"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profile"


class OTP(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    secret_key = models.CharField(max_length=32, blank=True)
    verified = models.BooleanField(default=False)
    last_used = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "OTP"
        verbose_name_plural = "OTPs"

    @classmethod
    def generate_otp(cls, user):
        otp, created = cls.objects.get_or_create(user=user)

        # generate 32 byte random secret key
        secret_key = pyotp.random_base32()
        otp.secret_key = secret_key
        otp.save()
        totp = pyotp.TOTP(secret_key, interval=120)
        otp_code = totp.now()

        return otp_code
