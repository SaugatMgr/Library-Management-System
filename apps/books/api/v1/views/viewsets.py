from django.db import transaction

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.books.api.v1.repository import (
    BookRepository,
    BorrowRepository,
    ReserveRepository,
)
from apps.books.api.v1.serializers.get import (
    BookListDetailSerializer,
    BorrowSerializer,
    GenreSerializer,
    NotificationSerializer,
    RatingSerializer,
    ReserveSerializer,
)
from apps.books.api.v1.serializers.post import (
    BookCreateUpdateSerializer,
    UpdateReserveStatusSerializer,
)

from apps.books.helpers.book_recommendations import (
    BookRecommender,
)
from apps.books.models import Book, Borrow, Genre, Notification, Rating, Reserve
from utils.helpers import get_instance_by_attr
from utils.pagination import CustomPageSizePagination
from utils.permissions import (
    LibrarianOrAdminPermission,
    NotificationUserOrLibrarianOrAdminPermission,
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
    }
    pagination_class = CustomPageSizePagination

    def get_queryset(self):
        return BookRepository.get_all()

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

    @action(detail=True, methods=["get"], url_path="recommended-books")
    def recommended_books(self, request, *args, **kwargs):
        book_id = kwargs.get("pk")
        book = get_instance_by_attr(Book, "id", book_id)

        recommender = BookRecommender()
        recommendations = recommender.recommend(book.id)

        return Response({"recommended_books": recommendations})


class BorrowModelViewSet(ModelViewSet):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer
    pagination_class = CustomPageSizePagination

    def get_queryset(self):
        return BorrowRepository.get_all()


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
    serializer_class = NotificationSerializer
    pagination_class = CustomPageSizePagination
    permission_classes = [NotificationUserOrLibrarianOrAdminPermission]

    def retrieve(self, request, *args, **kwargs):
        notification = self.get_object()
        if notification.user == request.user:
            notification.is_read = True
            notification.save()
        return super().retrieve(request, *args, **kwargs)
