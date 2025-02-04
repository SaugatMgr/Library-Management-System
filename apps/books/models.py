from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.academic.models import LibrarySection, Shelf
from utils.constants import (
    BookStatusChoices,
    BorrowStatusChoices,
    ReserveStatusChoices,
)
from utils.models import CommonInfo, CommonPaymentFields, NameField

User = get_user_model()


class Genre(NameField):
    pass


class Book(CommonInfo):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=150)
    publisher = models.CharField(max_length=255)
    publication_date = models.DateTimeField(blank=True, null=True)
    description = models.TextField()
    cover = models.ImageField(upload_to="books/cover/", blank=True, null=True)
    pages = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    isbn = models.CharField(max_length=17, unique=True)
    availability_status = models.CharField(
        choices=BookStatusChoices.choices,
        max_length=11,
        default=BookStatusChoices.AVAILABLE,
    )
    genres = models.ManyToManyField(Genre)
    section = models.ForeignKey(
        LibrarySection,
        on_delete=models.CASCADE,
        related_name="books",
        blank=True,
        null=True,
    )
    shelf = models.ForeignKey(
        Shelf, on_delete=models.CASCADE, related_name="books", blank=True, null=True
    )

    class Meta:
        unique_together = ["title", "isbn"]
        ordering = ["-created_on"]

    def __str__(self) -> str:
        return self.title


class Borrow(CommonInfo):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="borrow_set"
    )
    borrowed_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    returned_date = models.DateTimeField(null=True, blank=True)
    borrow_status = models.CharField(
        choices=BorrowStatusChoices.choices,
        max_length=12,
        default=BorrowStatusChoices.NOT_RETURNED,
    )
    overdue = models.BooleanField(default=False)

    class Meta:
        ordering = ["-borrowed_date"]

    def __str__(self) -> str:
        return f"{self.book} -- {self.borrower.get_full_name}"


class Reserve(CommonInfo):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reserver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reserve_set"
    )
    reserved_date = models.DateTimeField(default=timezone.now)
    reserve_status = models.CharField(
        choices=ReserveStatusChoices.choices,
        max_length=9,
        default=ReserveStatusChoices.PENDING,
    )
    reason = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.book} -- {self.reserver.get_full_name}"


class ReserveQueue(models.Model):
    book = models.OneToOneField(
        Book, on_delete=models.CASCADE, related_name="reserve_queue"
    )
    users = models.JSONField(default=list)

    class Meta:
        verbose_name = "Reserve Queue"
        verbose_name_plural = "Reserve Queue"

    def __str__(self) -> str:
        return f"{self.book} -- Queue"


class Notification(CommonInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField()
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self) -> str:
        return f"Notification for {self.user} -- {self.timestamp}"


class FinePayment(CommonPaymentFields):
    borrow = models.ForeignKey(
        Borrow,
        on_delete=models.CASCADE,
        verbose_name=_("Borrow"),
        related_name="fine_payments",
    )

    def __str__(self):
        return f"Fine Payment #{self.transaction_id}"

    class Meta:
        ordering = ["-created_on"]
        verbose_name = _("Fine Payment")
        verbose_name_plural = _("Fine Payments")


class Rating(CommonInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="ratings")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        unique_together = ["user", "book"]

    def __str__(self) -> str:
        return f"{self.user.get_full_name} -- {self.book} -- {self.rating}"
