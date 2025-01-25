from rest_framework import serializers

from apps.academic.api.v1.serializers.general import (
    LibrarySectionSerializer,
    ShelfSerializer,
)
from apps.books.models import (
    Book,
    Borrow,
    FinePayment,
    Genre,
    Notification,
    Rating,
    Reserve,
)
from apps.users.api.v1.serializers.get import UserListSerializer


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class BookListDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(read_only=True, many=True)
    section = LibrarySectionSerializer(read_only=True)
    shelf = ShelfSerializer(read_only=True)

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "publisher",
            "publication_date",
            "description",
            "cover",
            "pages",
            "price",
            "quantity",
            "isbn",
            "availability_status",
            "genres",
            "section",
            "shelf",
            "created_on",
            "modified_on",
        )


class BorrowSerializer(serializers.ModelSerializer):
    book = BookListDetailSerializer()
    borrower = UserListSerializer()

    class Meta:
        model = Borrow
        fields = (
            "id",
            "book",
            "borrower",
            "borrowed_date",
            "due_date",
            "returned_date",
            "borrow_status",
            "overdue",
        )


class BorrowForFineSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField()
    borrower = serializers.StringRelatedField()

    class Meta:
        model = Borrow
        fields = (
            "id",
            "book",
            "borrower",
            "borrowed_date",
            "due_date",
            "returned_date",
            "borrow_status",
            "overdue",
        )


class ReserveSerializer(serializers.ModelSerializer):
    book = BookListDetailSerializer()
    reserver = UserListSerializer()

    class Meta:
        model = Reserve
        fields = (
            "id",
            "book",
            "reserver",
            "reserved_date",
            "reserve_status",
            "reason",
        )


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = (
            "id",
            "book",
            "user",
            "rating",
        )
        read_only_fields = ("id",)


class ExportDataSerializer(serializers.Serializer):
    count = serializers.IntegerField(required=False)
    format = serializers.ChoiceField(choices=["csv", "excel"], required=True)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"


class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "message",
            "timestamp",
            "is_read",
        ]


class FinePaymentSerializer(serializers.ModelSerializer):
    borrow = BorrowForFineSerializer(read_only=True)

    class Meta:
        model = FinePayment
        fields = [
            "id",
            "borrow",
            "amount",
            "payment_method",
            "status",
            "transaction_id",
        ]


class FinePaymentDetailSerializer(serializers.ModelSerializer):
    borrow = BorrowSerializer(read_only=True)

    class Meta:
        model = FinePayment
        fields = [
            "id",
            "borrow",
            "amount",
            "payment_method",
            "status",
            "transaction_id",
        ]
