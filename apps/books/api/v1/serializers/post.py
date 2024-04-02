from rest_framework import serializers

from apps.books.models import Book, Reserve
from apps.users.models import CustomUser
from utils.constants import ReserveStatusChoices


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


class UpdateReserveStatusSerializer(serializers.ModelSerializer):
    reserver = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter())
    reserve_status = serializers.ChoiceField(choices=ReserveStatusChoices.choices)

    class Meta:
        model = Reserve
        fields = (
            "reserver",
            "reserve_status",
            "reason",
        )
