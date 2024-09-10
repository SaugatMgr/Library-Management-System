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


class DigitalResourceTypeChoices(models.TextChoices):
    VIDEO = "video", "Video"
    AUDIO = "audio", "Audio"
    PDF = "pdf", "pdf"
    INTERACTIVE = "interactive", "Interactive"


class MemberShipPlanChoices(models.TextChoices):
    MONTHLY = "monthly", "Monthly"
    YEARLY = "yearly", "Yearly"
    LIFETIME = "lifetime", "Lifetime"


class SemesterChoices(models.TextChoices):
    FIRST = "First"
    SECOND = "Second"
    THIRD = "Third"
    FOURTH = "Fourth"
    FIFTH = "Fifth"
    SIXTH = "Sixth"
    SEVENTH = "Seventh"
    EIGHTH = "Eighth"


class PaymentMethodChoices(models.TextChoices):
    KHALTI = "khalti", "Khalti"
    ESEWA = "esewa", "eSewa"


class PaymentStatusChoices(models.TextChoices):
    PENDING = "Pending"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    FAILED = "Failed"
    REFUNDED = "Refunded"
    PARTIAL = "Partial"
    REJECTED = "Rejected"
