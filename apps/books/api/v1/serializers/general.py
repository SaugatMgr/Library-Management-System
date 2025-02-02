from rest_framework import serializers

from apps.books.models import FinePayment


class FinePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinePayment
        fields = [
            "id",
            "borrow",
            "amount",
            "transaction_id",
            "payment_method",
            "status",
        ]
