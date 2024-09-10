from django.contrib import admin
from .models import Grade, Department, LibrarySection, Shelf, Staff, Student, Teacher


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ["name", "created_on"]
    search_fields = ["name"]
    ordering = ["-created_on"]


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "head_of_department",
        "phone_number",
        "borrowing_period_days",
    ]
    search_fields = ["name", "head_of_department", "phone_number"]
    ordering = ["-created_on"]


@admin.register(LibrarySection)
class LibrarySectionAdmin(admin.ModelAdmin):
    list_display = ["name", "location", "created_on"]
    search_fields = ["name", "location"]
    ordering = ["-created_on"]


@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    list_display = ["number", "section", "created_on"]
    search_fields = ["number", "section__name"]
    ordering = ["-created_on"]


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = [
        "get_full_name",
        "employee_id",
        "department",
        "role",
        "borrowing_period_days",
    ]
    search_fields = [
        "user__first_name",
        "user__middle_name",
        "user__last_name",
        "employee_id",
        "department__name",
        "role",
    ]
    ordering = ["-created_on"]

    def get_full_name(self, obj):
        return (
            f"{obj.user.first_name} {obj.user.middle_name or ''} {obj.user.last_name}"
        )

    get_full_name.short_description = "Full Name"


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        "get_full_name",
        "roll_number",
        "registration_number",
        "symbol_number",
        "department",
        "grade",
        "semester",
    ]
    search_fields = [
        "user__first_name",
        "user__middle_name",
        "user__last_name",
        "roll_number",
        "registration_number",
        "symbol_number",
        "department__name",
    ]
    ordering = ["-created_on"]

    def get_full_name(self, obj):
        return (
            f"{obj.user.first_name} {obj.user.middle_name or ''} {obj.user.last_name}"
        )

    get_full_name.short_description = "Full Name"


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = [
        "get_full_name",
        "employee_id",
        "department",
        "designation",
        "borrowing_period_days",
    ]
    search_fields = [
        "user__first_name",
        "user__middle_name",
        "user__last_name",
        "employee_id",
        "department__name",
        "designation",
    ]
    ordering = ["-created_on"]

    def get_full_name(self, obj):
        return (
            f"{obj.user.first_name} {obj.user.middle_name or ''} {obj.user.last_name}"
        )

    get_full_name.short_description = "Full Name"
