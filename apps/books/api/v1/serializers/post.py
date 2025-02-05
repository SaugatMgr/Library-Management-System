from rest_framework import serializers

from apps.books.models import Book, Borrow, FinePayment, Notification, Reserve
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


class NotificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "message",
            "timestamp",
        ]


class FinePaymentCreateSerializer(serializers.ModelSerializer):
    borrow = serializers.PrimaryKeyRelatedField(queryset=Borrow.objects.all())

    class Meta:
        model = FinePayment
        fields = [
            "borrow",
            "amount",
            "payment_method",
            "status",
            "transaction_id",
        ]


class FinePaymentUpdateSerializer(serializers.ModelSerializer):
    borrow = serializers.PrimaryKeyRelatedField(queryset=Borrow.objects.all())

    class Meta:
        model = FinePayment
        fields = [
            "borrow",
            "amount",
            "payment_method",
        ]
