from rest_framework.viewsets import ModelViewSet

from apps.academic.api.v1.serializers.general import (
    DepartmentSerializer,
    GradeSerializer,
    LibrarySectionSerializer,
    ShelfSerializer,
    StaffSerializer,
    StudentSerializer,
    TeacherSerializer,
)
from apps.academic.api.v1.serializers.get import (
    ShelfDetailSerializer,
    StaffDetailSerializer,
    StudentDetailSerializer,
    TeacherDetailSerializer,
)
from apps.academic.models import (
    Department,
    Grade,
    LibrarySection,
    Shelf,
    Student,
    Teacher,
    Staff,
)
from utils.pagination import CustomPageSizePagination


class GradeViewSet(ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    pagination_class = CustomPageSizePagination


class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    pagination_class = CustomPageSizePagination


class LibrarySectionViewSet(ModelViewSet):
    queryset = LibrarySection.objects.all()
    serializer_class = LibrarySectionSerializer
    pagination_class = CustomPageSizePagination


class ShelfViewSet(ModelViewSet):
    queryset = Shelf.objects.all()
    serializer_class = ShelfSerializer
    pagination_class = CustomPageSizePagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ShelfDetailSerializer
        return super().get_serializer_class()


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = CustomPageSizePagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return StudentDetailSerializer
        return super().get_serializer_class()


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    pagination_class = CustomPageSizePagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TeacherDetailSerializer
        return super().get_serializer_class()


class StaffViewSet(ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    pagination_class = CustomPageSizePagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return StaffDetailSerializer
        return super().get_serializer_class()
