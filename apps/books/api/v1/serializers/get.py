from rest_framework import serializers

from apps.books.models import Book, Borrow, Genre, Reserve, Tag
from apps.users.api.v1.serializers.get import UserListSerializer


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class BookListDetailSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    tag = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "publisher",
            "publication_year",
            "description",
            "cover",
            "pages",
            "price",
            "quantity",
            "isbn",
            "availability_status",
            "genre",
            "tag",
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
