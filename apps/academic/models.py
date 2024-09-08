from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model

from utils.constants import SemesterChoices
from utils.models import CommonInfo, NameField

User = get_user_model()


class Grade(NameField):
    class Meta:
        verbose_name = _("Grade")
        verbose_name_plural = _("Grades")
        ordering = ["-created_at"]


class Department(NameField):
    head_of_department = models.CharField(
        max_length=100,
        verbose_name=_("Head of Department"),
    )
    description = models.TextField(_("description"), blank=True, null=True)
    phone_number = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        null=True,
        verbose_name=_("Phone No."),
        validators=[
            RegexValidator(r"^\d{10}$", "Enter a valid 10-digit phone number.")
        ],
    )
    location = models.CharField(_("location"), max_length=255, blank=True, null=True)
    borrowing_period_days = models.PositiveIntegerField(
        default=90, verbose_name=_("Borrowing Period (Days)")
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")
        ordering = ["-created_at"]


class Staff(CommonInfo):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(
        max_length=50, unique=True, verbose_name=_("Employee ID")
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Department"),
    )
    role = models.CharField(max_length=100, verbose_name=_("Role"))
    authorized_sections = models.ManyToManyField(
        "books.Section",
        related_name="authorized_staff",
        blank=True,
        verbose_name=_("Authorized Sections"),
    )
    tasks = models.TextField(blank=True, verbose_name=_("Tasks"))
    borrowing_period_days = models.PositiveIntegerField(
        default=30, verbose_name=_("Borrowing Period (Days)")
    )

    def __str__(self) -> str:
        return f"{self.user.get_full_name} - {self.employee_id}"

    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staffs"
        ordering = ["-created_at"]


class Student(CommonInfo):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.PositiveIntegerField(verbose_name=_("Roll No."))
    registration_number = models.CharField(
        max_length=50, unique=True, verbose_name=_("Registration No.")
    )
    symbol_number = models.CharField(
        max_length=50, unique=True, verbose_name=_("Symbol No.")
    )
    grade = models.ForeignKey(
        Grade,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Grade"),
    )
    department = models.ForeignKey(
        "academic.Department",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Department"),
    )
    semester = models.CharField(
        choices=SemesterChoices.choices, verbose_name=_("Semester")
    )
    borrowing_period_days = models.PositiveIntegerField(
        default=14, verbose_name=_("Borrowing Period (Days)")
    )

    def __str__(self) -> str:
        return f"{self.user.get_full_name} - {self.roll_number}"

    class Meta:
        unique_together = (
            "user",
            "roll_number",
            "registration_number",
            "symbol_number",
        )
        verbose_name = "Student"
        verbose_name_plural = "Students"


class Teacher(CommonInfo):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(
        max_length=50, unique=True, verbose_name=_("Employee ID")
    )
    grade = models.ForeignKey(
        Grade,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Grade"),
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Department"),
    )
    designation = models.CharField(max_length=100, verbose_name=_("Designation"))
    borrowing_period_days = models.PositiveIntegerField(
        default=60, verbose_name=_("Borrowing Period (Days)")
    )

    def __str__(self) -> str:
        return f"{self.user.get_full_name} - {self.employee_id}"

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
        ordering = ["-created_at"]
