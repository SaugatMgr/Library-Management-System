import base64
import json
import requests

from datetime import timedelta

from django.db import transaction
from django.urls import reverse
from django.utils import timezone
from django.conf import settings

from rest_framework import serializers, status
from rest_framework.exceptions import NotAcceptable
from rest_framework.response import Response

from apps.books.api.v1.serializers.general import FinePaymentSerializer
from apps.books.helpers.error_messages import (
    ALREADY_BORROWED,
    ALREADY_RESERVED,
    OUT_OF_STOCK,
)
from apps.books.helpers.payment import generate_hmac_signature, generate_transaction_id
from apps.books.models import Book, Borrow, Reserve, ReserveQueue
from apps.books.tasks import notify_book_available

from apps.users.models import CustomUser
from utils.constants import (
    BookStatusChoices,
    BorrowStatusChoices,
    PaymentMethodChoices,
    PaymentStatusChoices,
    ReserveStatusChoices,
)
from utils.helpers import generate_error, get_instance_by_attr
from utils.threads import get_current_user


class BookRepository:
    @classmethod
    def get_all(cls):
        return Book.objects.filter()

    @staticmethod
    def borrow_book(data):
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

    @staticmethod
    def generate_esewa_form_data(data):
        borrow_id = data.get("borrow_id")
        product_code = settings.ESEWA_MERCHANT_ID
        message = (
            f"total_amount=110,transaction_uuid={borrow_id},product_code={product_code}"
        )
        hmac_signature = generate_hmac_signature(settings.ESEWA_SECRET, message)

        return {
            "amount": "100",
            "tax_amount": "10",
            "total_amount": "110",
            "transaction_uuid": f"{borrow_id}",
            "product_code": f"{product_code}",
            "product_service_charge": "0",
            "product_delivery_charge": "0",
            "success_url": f"http://127.0.0.1:8000/api/v1/borrow/{borrow_id}/payment/esewa/verify",
            "failure_url": f"http://localhost:5173/payment/esewa/{borrow_id}",
            "signed_field_names": "total_amount,transaction_uuid,product_code",
            "signature": f"{hmac_signature}",
        }

    @staticmethod
    def calculate_total_fine(borrow):
        days_passed = (timezone.now() - borrow.due_date).days
        return days_passed * settings.FINE_PER_DAY

    @classmethod
    def pay_with_esewa(cls, id, data):
        try:
            get_response_decoded_data = base64.b64decode(data).decode("utf-8")
            get_response_decoded_data = json.loads(get_response_decoded_data)

            get_url = (
                f"{settings.ESEWA_VERIFY_URL}"
                f"?product_code={settings.ESEWA_MERCHANT_ID}"
                f"&total_amount={get_response_decoded_data.get('total_amount')}"
                f"&transaction_uuid={get_response_decoded_data.get('transaction_uuid')}"
            )

            with transaction.atomic():
                response = requests.get(get_url)
                response = response.json()

                if response.get("status") == "COMPLETE" and response.get("ref_id"):
                    borrow = get_instance_by_attr(Borrow, "id", id)
                    payment_data = {
                        "borrow": id,
                        "amount": cls.calculate_total_fine(borrow),
                        "payment_method": PaymentMethodChoices.ESEWA,
                        "status": PaymentStatusChoices.COMPLETED,
                        "transaction_id": generate_transaction_id(),
                    }
                    payment_serializer = FinePaymentSerializer(data=payment_data)
                    payment_serializer.is_valid(raise_exception=True)
                    payment_serializer.save()

                    borrow.overdue = False
                    borrow.save()
                else:
                    raise serializers.ValidationError(
                        generate_error(
                            message="Payment not completed.",
                            code="payment_not_completed",
                        )
                    )
        except Exception:
            raise serializers.ValidationError(
                generate_error(
                    message="Error occurred while processing payment.",
                    code="payment_error",
                )
            )

    @classmethod
    def initiate_khalti_payment(cls, request, data, borrow_id):
        data["return_url"] = request.build_absolute_uri(
            reverse("borrow-verify-khalti-payment", kwargs={"pk": borrow_id}),
        )
        data["amount"] = cls.calculate_total_fine(
            get_instance_by_attr(Borrow, "id", borrow_id)
        )
        data = json.dumps(data)
        url = settings.KHALTI_INITIATE_URL
        headers = {
            "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(url, data=data, headers=headers)
            return Response(response.json(), status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def pay_with_khalti(cls, data, borrow_id):
        if not (
            "pidx" in data
            or "transaction_id" in data
            or "tidx" in data
            or "amount" in data
        ):
            raise serializers.ValidationError(
                generate_error(
                    message="Missing required information.",
                    code="missing_required_fields",
                )
            )
        try:
            with transaction.atomic():
                verify_url = settings.KHALTI_VERIFY_URL
                headers = {
                    "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
                    "Content-Type": "application/json",
                }
                response = requests.post(
                    verify_url,
                    json={"pidx": data.get("pidx")},
                    headers=headers,
                ).json()

                if response.get("status") == "Completed" and response.get("pidx"):
                    borrow = get_instance_by_attr(Borrow, "id", borrow_id)
                    payment_data = {
                        "borrow": borrow_id,
                        "amount": cls.calculate_total_fine(borrow),
                        "payment_method": PaymentMethodChoices.KHALTI,
                        "status": PaymentStatusChoices.COMPLETED,
                        "transaction_id": generate_transaction_id(),
                    }
                    payment_serializer = FinePaymentSerializer(data=payment_data)
                    payment_serializer.is_valid(raise_exception=True)
                    payment_serializer.save()

                    borrow.overdue = False
                    borrow.save()
                else:
                    raise serializers.ValidationError(
                        generate_error(
                            message="Payment not completed.",
                            code="payment_not_completed",
                        )
                    )
        except Exception as _:
            raise serializers.ValidationError(
                generate_error(
                    message="Error occurred while processing payment.",
                    code="payment_error",
                )
            )


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
