from datetime import timedelta
from django.utils import timezone
from rest_framework.exceptions import NotAcceptable

from apps.books.models import Book, Borrow
from utils.constants import BookStatusChoices
from utils.helpers import generate_error, get_instance_by_attr


class BookRepository:
    @classmethod
    def get_all(cls):
        return Book.objects.filter()

    @classmethod
    def borrow_book(cls, data):
        book = get_instance_by_attr(Book, "id", data["book_id"])
        if book.quantity == 0:
            raise NotAcceptable(
                generate_error(
                    message="Book is out of stock.", code="book_out_of_stock"
                )
            )
        if book.availability_status == BookStatusChoices.UNAVAILABLE:
            raise NotAcceptable(
                generate_error(
                    message="Book is not available.", code="book_unavailable"
                )
            )
        borrow_data = {
            "book_id": book.id,
            "borrower_id": data["borrower"].id,
            "due_date": data["days"],
        }
        BorrowRepository.create(borrow_data)
        book.quantity -= 1
        book.save()
        if book.quantity == 0:
            book.availability_status = BookStatusChoices.UNAVAILABLE
            book.save()


class BorrowRepository:
    @classmethod
    def get_all(cls):
        return Borrow.objects.filter()

    @classmethod
    def create(cls, data):
        if Borrow.objects.filter(
            book_id=data["book_id"], borrower_id=data["borrower_id"]
        ).exists():
            raise NotAcceptable(
                generate_error(
                    message="You have already borrowed this book.",
                    code="already_borrowed",
                )
            )
        due_date = timezone.now() + timedelta(days=int(data.pop("due_date")))
        data["due_date"] = due_date
        Borrow.objects.create(**data)
