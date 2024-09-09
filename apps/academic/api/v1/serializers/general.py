from rest_framework import serializers

from apps.academic.models import (
    Department,
    Grade,
    LibrarySection,
    Shelf,
    Staff,
    Teacher,
)


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


class LibrarySectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibrarySection
        fields = (
            "id",
            "name",
            "description",
            "location",
        )


class ShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelf
        fields = (
            "id",
            "number",
            "description",
            "section",
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


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = (
            "id",
            "user",
            "employee_id",
            "department",
            "role",
            "authorized_sections",
            "tasks",
            "borrowing_period_days",
        )
