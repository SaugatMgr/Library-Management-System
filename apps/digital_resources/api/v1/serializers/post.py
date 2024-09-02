from rest_framework import serializers

from apps.digital_resources.models import DigitalResource
from utils.helpers import compare_resource_type_with_uploaded_file


class DigitalResourceCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalResource
        fields = "__all__"

    def validate(self, data):
        file_name = data.get("file").name
        resource_type = data.get("resource_type")

        mime_type, resource_type_file_match = compare_resource_type_with_uploaded_file(
            file_name, resource_type
        )
        if not resource_type_file_match:
            raise serializers.ValidationError(
                f"The uploaded file type ({mime_type}) does not match the selected resource type ({resource_type})."
            )
        return data
