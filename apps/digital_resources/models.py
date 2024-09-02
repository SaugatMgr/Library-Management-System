from django.db import models

from utils.constants import DigitalResourceTypeChoices
from utils.models import CommonInfo


class DigitalResource(CommonInfo):
    title = models.CharField(max_length=255)
    resource_type = models.CharField(
        max_length=11, choices=DigitalResourceTypeChoices.choices
    )
    file = models.FileField(upload_to="digital_resources/")
    description = models.TextField(null=True, blank=True)
    related_books = models.ManyToManyField(
        "books.Book", related_name="digital_resources", blank=True
    )

    def __str__(self) -> str:
        return self.title
