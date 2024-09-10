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


class GradeViewSet(ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer


class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class LibrarySectionViewSet(ModelViewSet):
    queryset = LibrarySection.objects.all()
    serializer_class = LibrarySectionSerializer


class ShelfViewSet(ModelViewSet):
    queryset = Shelf.objects.all()
    serializer_class = ShelfSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ShelfDetailSerializer
        return super().get_serializer_class()


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return StudentDetailSerializer
        return super().get_serializer_class()


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TeacherDetailSerializer
        return super().get_serializer_class()


class StaffViewSet(ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return StaffDetailSerializer
        return super().get_serializer_class()
