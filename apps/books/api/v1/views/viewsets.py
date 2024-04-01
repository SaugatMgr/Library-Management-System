from django.db import transaction

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from apps.books.api.v1.repository import (
    BookRepository,
    BorrowRepository,
    ReserveRepository,
)
from apps.books.api.v1.serializers.get import (
    BookListDetailSerializer,
    BorrowSerializer,
    GenreSerializer,
    ReserveSerializer,
    TagSerializer,
)
from apps.books.api.v1.serializers.post import BookCreateUpdateSerializer
from apps.books.models import Borrow, Genre, Reserve, Tag
from utils.helpers import to_internal_value


class GenreModelViewSet(ModelViewSet):
    queryset = Genre.objects.filter()
    serializer_class = GenreSerializer


class TagModelViewSet(ModelViewSet):
    queryset = Tag.objects.filter()
    serializer_class = TagSerializer


class BookModelViewSet(ModelViewSet):
    serializer_action = {
        "list": BookListDetailSerializer,
        "retrieve": BookListDetailSerializer,
        "create": BookCreateUpdateSerializer,
        "update": BookCreateUpdateSerializer,
    }

    def get_queryset(self):
        return BookRepository.get_all()

    def get_serializer_class(self):
        return self.serializer_action.get(self.action)

    def create(self, request, *args, **kwargs):
        data = request.data
        cover = data.pop("cover")
        if cover:
            data["cover"] = to_internal_value(cover)
        book_serializer = self.get_serializer(data=data)
        book_serializer.is_valid(raise_exception=True)
        book_serializer.save()
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


class BorrowModelViewSet(ModelViewSet):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer

    def get_queryset(self):
        return BorrowRepository.get_all()


class ReserveModelViewSet(ModelViewSet):
    queryset = Reserve.objects.all()
    serializer_class = ReserveSerializer

    def get_queryset(self):
        return ReserveRepository.get_all()

    @action(detail=True, methods=["post"], url_path="update-reservation-status")
    def update_reservation_status(self, request, *args, **kwargs):
        reserve_status = request.data["reserve_status"]
        reason = request.data.get("reason")
        ReserveRepository.update_reservation_status(
            kwargs["pk"], reserve_status, reason
        )
        return Response({"message": "Reservation status updated successfully."})
