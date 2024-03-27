from rest_framework import serializers

from apps.books.models import Book


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "title",
            "author",
            "publisher",
            "description",
            "cover",
            "pages",
            "price",
            "quantity",
            "isbn",
            "genre",
            "tag",
        )
