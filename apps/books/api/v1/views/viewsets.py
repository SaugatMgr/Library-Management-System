import json

from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect

from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.books.api.v1.repository import (
    BookRepository,
    BorrowRepository,
    ReserveRepository,
)
from apps.books.api.v1.serializers.get import (
    BookListDetailSerializer,
    BorrowSerializer,
    FinePaymentDetailSerializer,
    FinePaymentSerializer,
    GenreSerializer,
    NotificationSerializer,
    RatingSerializer,
    ReserveSerializer,
)
from apps.books.api.v1.serializers.post import (
    BookCreateUpdateSerializer,
    FinePaymentCreateSerializer,
    FinePaymentUpdateSerializer,
    NotificationUpdateSerializer,
    UpdateReserveStatusSerializer,
)

from apps.books.helpers.book_recommendations import (
    BookRecommender,
)
from apps.books.helpers.payment import generate_transaction_id
from apps.books.models import (
    Book,
    Borrow,
    FinePayment,
    Genre,
    Notification,
    Rating,
    Reserve,
)

from utils.helpers import generate_error, get_instance_by_attr
from utils.pagination import CustomPageSizePagination
from utils.permissions import (
    LibrarianOrAdminPermission,
)


class GenreModelViewSet(ModelViewSet):
    queryset = Genre.objects.filter()
    serializer_class = GenreSerializer
    pagination_class = CustomPageSizePagination


class BookModelViewSet(ModelViewSet):
    serializer_action = {
        "list": BookListDetailSerializer,
        "retrieve": BookListDetailSerializer,
        "create": BookCreateUpdateSerializer,
        "update": BookCreateUpdateSerializer,
        "recommended_books": BookListDetailSerializer,
    }
    action_permissions = {
        "create": [LibrarianOrAdminPermission],
        "list": [AllowAny],
        "retrieve": [AllowAny],
        "update": [LibrarianOrAdminPermission],
        "destroy": [LibrarianOrAdminPermission],
        "borrow_book": [IsAuthenticated],
        "reserve_book": [IsAuthenticated],
        "return_book": [IsAuthenticated],
        "recommended_books": [AllowAny],
    }
    pagination_class = CustomPageSizePagination

    def get_queryset(self):
        query = self.request.query_params.get("query")
        all_books = BookRepository.get_all()
        if query:
            filtered_queryset = all_books.filter(
                Q(title__icontains=query)
                | Q(author__icontains=query)
                | Q(genres__name__icontains=query)
                | Q(isbn=query)
                | Q(publisher__icontains=query)
            ).distinct()
            return filtered_queryset
        return all_books

    def get_serializer_class(self):
        return self.serializer_action.get(self.action)

    def get_permissions(self):
        return [
            permission()
            for permission in self.action_permissions.get(
                self.action, [LibrarianOrAdminPermission]
            )
        ]

    def create(self, request, *args, **kwargs):
        data = request.data
        genres_list = json.loads(data["genres"])
        data.pop("genres")

        book_serializer = self.get_serializer(data=data)
        book_serializer.is_valid(raise_exception=True)
        book = book_serializer.save()

        genres = Genre.objects.filter(id__in=genres_list)
        book.genres.set(genres)
        return Response({"message": "Book created successfully"}, status=201)

    def update(self, request, *args, **kwargs):
        data = request.data
        book_serializer = self.get_serializer(
            instance=self.get_object(), data=data, partial=True
        )
        book_serializer.is_valid(raise_exception=True)
        book_serializer.save()
        return Response({"message": "Book updated successfully."}, status=200)

    @action(detail=True, methods=["post"], url_path="borrow-book")
    def borrow_book(self, request, *args, **kwargs):
        with transaction.atomic():
            data = {
                "days": request.data["days"],
                "book_id": kwargs.get("pk"),
                "borrower": request.user,
            }
            BookRepository.borrow_book(data)
            return Response({"message": "Book borrowed successfully."})

    @action(detail=False, methods=["post"], url_path="return-book")
    def return_book(self, request, *args, **kwargs):
        with transaction.atomic():
            status = BookRepository.return_book(request.data["borrow_id"])
            if status:
                return Response({"message": "Book returned successfully."})
            return Response({"message": "The book has already been returned."})

    @action(detail=True, methods=["post"], url_path="reserve-book")
    def reserve_book(self, request, *args, **kwargs):
        with transaction.atomic():
            data = {
                "book_id": kwargs.get("pk"),
                "user": request.user,
            }
            response = BookRepository.reserve_book(data)
            return response

    @action(detail=True, methods=["get"], url_path="recommended-books")
    def recommended_books(self, request, *args, **kwargs):
        book_id = kwargs.get("pk")
        book = get_instance_by_attr(Book, "id", book_id)

        recommender = BookRecommender()
        recommendations = recommender.recommend(book.id)

        for data in recommendations:
            current_book = get_instance_by_attr(Book, "id", data["id"])
            data["cover"] = current_book.cover.url

        return Response({"recommended_books": recommendations})


class BorrowModelViewSet(ModelViewSet):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer
    action_permissions = {
        "create": [IsAuthenticated],
        "list": [IsAuthenticated],
        "retrieve": [IsAuthenticated],
        "update": [LibrarianOrAdminPermission],
        "destroy": [LibrarianOrAdminPermission],
        "user_borrow_list": [IsAuthenticated],
        "initiate_esewa_payment": [IsAuthenticated],
        "verify_esewa_payment": [IsAuthenticated],
        "initiate_khalti_payment": [IsAuthenticated],
        "verify_khalti_payment": [IsAuthenticated],
    }
    pagination_class = CustomPageSizePagination

    def get_permissions(self):
        return [
            permission()
            for permission in self.action_permissions.get(
                self.action, [LibrarianOrAdminPermission]
            )
        ]

    @action(detail=False, methods=["get"], url_path="user-borrow-list")
    def user_borrow_list(self, request):
        user_id = self.request.query_params.get("user")
        user_borrows = BorrowRepository.get_borrowed_books_by_user(user_id)

        if user_borrows.exists():
            paginator = self.paginate_queryset(user_borrows)
            paginated_borrows = self.get_serializer(paginator, many=True).data
            return Response(self.get_paginated_response(paginated_borrows).data)
        return Response({"message": "You have not borrowed books yet."})

    @action(detail=False, methods=["post"], url_path="payment/esewa/initiate")
    def initiate_esewa_payment(self, request):
        data = request.data
        esewaFormData = BorrowRepository.generate_esewa_form_data(data)
        return Response(esewaFormData)

    @action(detail=True, methods=["get"], url_path="payment/esewa/verify")
    def verify_esewa_payment(self, request, *args, **kwargs):
        borrow_id = kwargs.get("pk")
        encoded_data = request.GET.get("data")
        BorrowRepository.pay_with_esewa(borrow_id, encoded_data)
        return HttpResponseRedirect("http://localhost:3000/user/borrow-history/")

    @action(detail=True, methods=["post"], url_path="payment/khalti/initiate")
    def initiate_khalti_payment(self, request, *args, **kwargs):
        data = request.data
        borrow_id = kwargs.get("pk")
        return BorrowRepository.initiate_khalti_payment(request, data, borrow_id)

    @action(detail=True, methods=["get"], url_path="payment/khalti/verify")
    def verify_khalti_payment(self, request, *args, **kwargs):
        data = request.GET.dict()
        borrow_id = kwargs.get("pk")
        BorrowRepository.pay_with_khalti(data, borrow_id)
        return HttpResponseRedirect("http://localhost:3000/user/borrow-history/")


class ReserveModelViewSet(ModelViewSet):
    queryset = Reserve.objects.all()
    serializer_class = ReserveSerializer
    pagination_class = CustomPageSizePagination

    def get_queryset(self):
        return ReserveRepository.get_all()

    @action(detail=True, methods=["post"], url_path="update-reservation-status")
    def update_reservation_status(self, request, *args, **kwargs):
        data = request.data
        update_reserve_status_serializer = UpdateReserveStatusSerializer(data=data)
        update_reserve_status_serializer.is_valid(raise_exception=True)
        validated_data = update_reserve_status_serializer.validated_data
        response = ReserveRepository.update_reservation_status(
            validated_data["reserver"],
            kwargs["pk"],
            validated_data["reserve_status"],
            validated_data.get("reason"),
        )
        return response


class RatingModelViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    pagination_class = CustomPageSizePagination


class NotificationModelViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_action = {
        "list": NotificationSerializer,
        "retrieve": NotificationSerializer,
        "create": NotificationSerializer,
        "update": NotificationUpdateSerializer,
    }
    action_permissions = {
        "list": [AllowAny],
        "create": [LibrarianOrAdminPermission],
        "retrieve": [AllowAny],
        "update": [LibrarianOrAdminPermission],
        "destroy": [LibrarianOrAdminPermission],
    }
    pagination_class = CustomPageSizePagination

    def get_serializer_class(self):
        return self.serializer_action.get(self.action)

    def get_permissions(self):
        return [
            permission()
            for permission in self.action_permissions.get(
                self.action, [LibrarianOrAdminPermission]
            )
        ]

    def retrieve(self, request, *args, **kwargs):
        notification = self.get_object()
        if notification.user == request.user:
            notification.is_read = True
            notification.save()
        return super().retrieve(request, *args, **kwargs)


class FinePaymentModelViewSet(ModelViewSet):
    queryset = FinePayment.objects.all()
    serializer_action = {
        "list": FinePaymentSerializer,
        "retrieve": FinePaymentDetailSerializer,
        "create": FinePaymentCreateSerializer,
        "update": FinePaymentUpdateSerializer,
    }
    action_permissions = {
        "list": [AllowAny],
        "create": [LibrarianOrAdminPermission],
        "retrieve": [AllowAny],
        "update": [LibrarianOrAdminPermission],
        "destroy": [LibrarianOrAdminPermission],
    }
    pagination_class = CustomPageSizePagination

    def get_serializer_class(self):
        return self.serializer_action.get(self.action)

    def get_permissions(self):
        return [
            permission()
            for permission in self.action_permissions.get(
                self.action, [LibrarianOrAdminPermission]
            )
        ]

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            data = request.data
            amount = data.get("amount")
            if data["payment_method"] == "cash" and not amount:
                raise serializers.ValidationError(
                    generate_error(
                        message="Amount is missing.",
                        code="amount_required",
                    )
                )
            data["transaction_id"] = generate_transaction_id()
            fine_payment_serializer = self.get_serializer(data=data)
            fine_payment_serializer.is_valid(raise_exception=True)
            fine_payment_serializer.save()

            borrow = fine_payment_serializer.validated_data["borrow"]
            borrow.overdue = False
            borrow.save()

            return Response(
                {"message": "Fine payment created successfully."}, status=201
            )

    def update(self, request, *args, **kwargs):
        with transaction.atomic():
            data = request.data
            fine_payment_serializer = self.get_serializer(
                instance=self.get_object(), data=data, partial=True
            )
            fine_payment_serializer.is_valid(raise_exception=True)
            fine_payment_serializer.save()
            return Response({"message": "Fine payment updated successfully."})
