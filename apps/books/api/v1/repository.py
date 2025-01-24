from datetime import timedelta

from django.utils import timezone

from rest_framework.exceptions import NotAcceptable
from rest_framework.response import Response

from apps.books.helpers.error_messages import (
    ALREADY_BORROWED,
    ALREADY_RESERVED,
    OUT_OF_STOCK,
)
from apps.books.models import Book, Borrow, Reserve, ReserveQueue
from apps.books.tasks import notify_book_available

from apps.users.models import CustomUser
from utils.constants import (
    BookStatusChoices,
    BorrowStatusChoices,
    ReserveStatusChoices,
)
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
            cls.get_all()
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
                user_id = ReserveQueueRepository.remove_from_queue(book)
                if user_id:
                    notify_book_available.delay(user_id, book.id)
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
        return Borrow.objects.filter()

    @classmethod
    def get_borrowed_books_by_user(cls, user_id):
        user = get_instance_by_attr(CustomUser, "id", user_id)
        return cls.get_all().filter(borrower=user)

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
    def update_reserve_fields(cls, reserve, reserve_status, reason):
        reserve.reserve_status = reserve_status
        reserve.reason = reason if reason else None
        reserve.save()

    @classmethod
    def update_reservation_status(cls, reserver, reserve_id, reserve_status, reason):
        reserve = get_instance_by_attr(Reserve, "id", reserve_id)
        accepted = ReserveStatusChoices.APPROVED
        rejected = ReserveStatusChoices.REJECTED
        cancelled = ReserveStatusChoices.CANCELLED

        if (reserve_status == rejected or reserve_status == cancelled) and not reason:
            return Response(
                {
                    "error": "Please provide a reason for rejecting or cancelling the reservation."
                },
                status=400,
            )
        if reserve_status == accepted:
            reserve_queue_data = {
                "book": reserve.book,
                "user": reserver,
            }
            cls.update_reserve_fields(reserve, reserve_status, reason)
            response = ReserveQueueRepository.add_to_queue(reserve_queue_data)

            return response
        cls.update_reserve_fields(reserve, reserve_status, reason)
        return Response({"message": "Reservation status updated successfully."})


class ReserveQueueRepository:
    @classmethod
    def get_all(cls):
        return ReserveQueue.objects.filter()

    @classmethod
    def add_to_queue(cls, data):
        book = data["book"]
        user = data["user"]
        user_id = str(user.id)
        reserve_queue, created = ReserveQueue.objects.get_or_create(book=book)
        users = reserve_queue.users

        if not users:
            reserve_queue.users = [user_id]
            reserve_queue.save()
        else:
            if user_id not in users:
                users.append(user_id)
                reserve_queue.save()
            else:
                return Response(
                    {"message": "You are already in the queue for this book."},
                    status=400,
                )
        return Response({"message": "You have been added to the queue."})

    @classmethod
    def remove_from_queue(cls, book):
        queue_of_book = cls.get_all().filter(book=book).first()
        if queue_of_book:
            users = queue_of_book.users
            if users:
                to_be_notified_user = users.pop(0)
                queue_of_book.save()
                return to_be_notified_user
