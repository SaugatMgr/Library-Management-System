from django.db import models
from django.core.exceptions import ValidationError

from utils.constants import DigitalResourceTypeChoices
from utils.helpers import compare_resource_type_with_uploaded_file
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

    def clean(self):
        file_name = self.file.name
        resource_type = self.resource_type

        mime_type, resource_type_file_match = compare_resource_type_with_uploaded_file(
            file_name, resource_type
        )
        if not resource_type_file_match:
            raise ValidationError(
                f"The uploaded file type ({mime_type}) does not match the selected resource type ({resource_type})."
            )

    def __str__(self) -> str:
        return self.title
