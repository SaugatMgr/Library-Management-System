from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

from utils.constants import BookStatusChoices
from utils.models import CommonInfo

User = get_user_model()


class NameField(CommonInfo):
    name = models.CharField(max_length=64)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Genre(NameField):
    pass


class Tag(NameField):
    pass


class Book(CommonInfo):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=64)
    publisher = models.CharField(max_length=255)
    description = models.TextField()
    cover = models.ImageField(upload_to="books/cover/", blank=True, null=True)
    pages = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    isbn = models.CharField(max_length=17)
    availability_status = models.CharField(
        choices=BookStatusChoices.choices,
        max_length=11,
        default=BookStatusChoices.AVAILABLE,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )
    tag = models.ManyToManyField(Tag)

    class Meta:
        unique_together = ["title", "isbn"]

    def __str__(self) -> str:
        return f"{self.author} -- {self.title}"


class Borrow(CommonInfo):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="borrowers"
    )
    borrowed_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.book} -- {self.borrower.get_full_name}"
