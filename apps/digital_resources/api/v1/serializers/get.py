from rest_framework import serializers

from apps.digital_resources.models import DigitalResource


class DigitalResourceListDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalResource
        fields = "__all__"
