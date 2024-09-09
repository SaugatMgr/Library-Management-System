from rest_framework import serializers

from apps.academic.models import Department, Grade


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = "name"


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = (
            "head_of_department",
            "description",
            "phone_number",
            "location",
            "borrowing_period_days",
        )
