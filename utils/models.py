import uuid
from django.db import models
from django.conf import settings

from utils.constants import PaymentMethodChoices, PaymentStatusChoices
from utils.threads import get_current_user


class CommonInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_created",
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_modified",
    )
    created_on = models.DateTimeField("created on", auto_now_add=True)
    modified_on = models.DateTimeField("last modified on", auto_now=True)

    def save(self, *args, **kwargs):
        from apps.users.models import CustomUser

        user = get_current_user()

        if isinstance(user, CustomUser):
            if not self.pk:
                self.created_by = user
            self.modified_by = user
        else:
            self.created_by = None
            self.modified_by = None

        super(CommonInfo, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class NameField(CommonInfo):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class CommonPaymentFields(CommonInfo):
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(
        max_length=6, choices=PaymentMethodChoices.choices
    )
    transaction_id = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(
        max_length=9,
        choices=PaymentStatusChoices.choices,
        default=PaymentStatusChoices.PENDING,
    )

    class Meta:
        abstract = True
