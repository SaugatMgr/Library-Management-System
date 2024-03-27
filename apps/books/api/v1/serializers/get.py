from rest_framework import serializers

from apps.books.models import Book, Genre, Tag


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
