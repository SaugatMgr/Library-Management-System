from datetime import timedelta
from django.utils import timezone

from rest_framework.exceptions import NotAcceptable
from rest_framework.response import Response

from apps.books.helpers.error_messages import (
    ALREADY_BORROWED,
    ALREADY_RESERVED,
    OUT_OF_STOCK,
)
from apps.books.models import Book, Borrow, Reserve
from utils.constants import BookStatusChoices, BorrowStatusChoices, ReserveStatusChoices
from utils.helpers import generate_error, get_instance_by_attr
from utils.threads import get_current_user


class BookRepository:
    @classmethod
    def get_all(cls):
        return Book.objects.filter()

    @classmethod
    def borrow_book(cls, data):
        book = get_instance_by_attr(Book, "id", data["book_id"])
        borrower = data["borrower"]
        if (
            BorrowRepository.get_all()
            .filter(
                book=book,
                borrower=borrower,
                borrow_status=BorrowStatusChoices.NOT_RETURNED,
            )
            .exists()
        ):
            raise NotAcceptable(ALREADY_BORROWED)
        if book.quantity == 0:
            raise NotAcceptable(OUT_OF_STOCK)
        if book.availability_status == BookStatusChoices.UNAVAILABLE:
            raise NotAcceptable(
                generate_error(
                    message="Book is not available.", code="book_unavailable"
                )
            )
        borrow_data = {
            "book_id": book.id,
            "borrower_id": borrower.id,
            "due_date": data["days"],
        }
        BorrowRepository.create(borrow_data)
        book.quantity -= 1
        book.save()
        if book.quantity == 0:
            book.availability_status = BookStatusChoices.UNAVAILABLE
            book.save()

    @classmethod
    def return_book(cls, borrow_id):
        borrow = get_instance_by_attr(Borrow, "id", borrow_id)
        if borrow.borrow_status == BorrowStatusChoices.NOT_RETURNED:
            book = borrow.book
            book.quantity += 1
            book.save()
            if book.availability_status == BookStatusChoices.UNAVAILABLE:
                book.availability_status = BookStatusChoices.AVAILABLE
                book.save()
            borrow.borrow_status = BorrowStatusChoices.RETURNED
            borrow.returned_date = timezone.now()
            borrow.save()
            return True
        else:
            return False

    @classmethod
    def reserve_book(cls, data):
        book = get_instance_by_attr(Book, "id", data["book_id"])
        is_borrowed = Borrow.objects.filter(
            book=book, borrow_status=BorrowStatusChoices.NOT_RETURNED
        ).exists()
        is_borrowed_by_current_user = (
            BorrowRepository.get_all()
            .filter(
                book=book,
                borrow_status=BorrowStatusChoices.NOT_RETURNED,
            )
            .exists()
        )
        is_reserved_by_current_user = (
            ReserveRepository.get_all()
            .filter(book=book, reserve_status=ReserveStatusChoices.PENDING)
            .exists()
        )
        quantity = book.quantity
        if quantity == 0 and not is_borrowed:
            raise NotAcceptable(OUT_OF_STOCK)
        if quantity > 0:
            return Response({"message": "Book is available for borrowing."})
        if is_borrowed_by_current_user:
            raise NotAcceptable(ALREADY_BORROWED)
        if is_reserved_by_current_user:
            raise NotAcceptable(ALREADY_RESERVED)

        reserve_data = {
            "book_id": book.id,
            "reserver_id": data["user"].id,
        }
        ReserveRepository.create(reserve_data)
        return Response({"message": "Book reserved successfully."})


class BorrowRepository:
    @classmethod
    def get_all(cls):
        return Borrow.objects.filter(borrower=get_current_user())

    @classmethod
    def create(cls, data):
        due_date = timezone.now() + timedelta(days=int(data.pop("due_date")))
        data["due_date"] = due_date
        Borrow.objects.create(**data)


class ReserveRepository:
    @classmethod
    def get_all(cls):
        return Reserve.objects.filter(reserver=get_current_user())

    @classmethod
    def create(cls, data):
        Reserve.objects.create(**data)

    @classmethod
    def update_reservation_status(cls, reserve_id, reserve_status, reason):
        reserve = get_instance_by_attr(Reserve, "id", reserve_id)
        if (
            reserve_status == ReserveStatusChoices.REJECTED
            or reserve_status == ReserveStatusChoices.CANCELLED
            and not reason
        ):
            return Response(
                {
                    "error": "Please provide a reason for rejecting or cancelling the reservation."
                },
                status=400,
            )
        reserve.reserve_status = reserve_status
        reserve.save()
