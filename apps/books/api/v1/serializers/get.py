from rest_framework import serializers

from apps.books.models import Book, Borrow, Genre, Rating, Reserve
from apps.users.api.v1.serializers.get import UserListSerializer


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class BookListDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(read_only=True, many=True)

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
