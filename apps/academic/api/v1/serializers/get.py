from rest_framework import serializers

from apps.academic.api.v1.serializers.general import (
    DepartmentSerializer,
    GradeSerializer,
    LibrarySectionSerializer,
)
from apps.academic.models import (
    Shelf,
    Teacher,
    Staff,
    Student,
)
from apps.users.api.v1.serializers.get import UserDetailSerializer


class ShelfDetailSerializer(serializers.ModelSerializer):
    section = LibrarySectionSerializer()

    class Meta:
        model = Shelf
        fields = (
            "id",
            "number",
            "description",
            "section",
        )


class StudentDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    grade = GradeSerializer()
    department = DepartmentSerializer()

    class Meta:
        model = Student
        fields = (
            "id",
            "user",
            "roll_number",
            "registration_number",
            "symbol_number",
            "grade",
            "department",
            "semester",
            "borrowing_period_days",
        )


class TeacherDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    grade = GradeSerializer()
    department = DepartmentSerializer()

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


class StaffDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    department = DepartmentSerializer()
    authorized_sections = LibrarySectionSerializer(many=True)

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
