from rest_framework import serializers

from apps.academic.models import Department, Grade, Staff, Teacher


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = (
            "id",
            "name",
        )


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = (
            "id",
            "head_of_department",
            "description",
            "phone_number",
            "location",
            "borrowing_period_days",
        )


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = (
            "id",
            "user",
            "employee_id",
            "grade",
            "department",
            "designation",
            "borrowing_period_days",
        )
