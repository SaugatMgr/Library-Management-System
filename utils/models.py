import uuid
from django.db import models
from django.conf import settings

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
        user = get_current_user()
        if user:
            if not self.pk:
                self.created_by = user
            self.modified_by = user

        super(CommonInfo, self).save(*args, **kwargs)

    class Meta:
        abstract = True
