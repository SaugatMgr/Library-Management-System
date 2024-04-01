from django.db import models


class UserGroupChoices(models.TextChoices):
    ADMIN = "Admin"
    LIBRARIAN = "Librarian"
    ASSISTANT_LIBRARIAN = "Assistant Librarian"


class GenderChoices(models.TextChoices):
    MALE = "M", "Male"
    FEMALE = "F", "Female"
    OTHERS = "O", "Others"


class BookStatusChoices(models.TextChoices):
    AVAILABLE = "Available"
    UNAVAILABLE = "Unavailable"


class BorrowStatusChoices(models.TextChoices):
    NOT_RETURNED = "Not Returned"
    RETURNED = "Returned"


class ReserveStatusChoices(models.TextChoices):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    CANCELLED = "Cancelled"
