from rest_framework.viewsets import ModelViewSet

from apps.academic.api.v1.serializers.general import (
    DepartmentSerializer,
    GradeSerializer,
    LibrarySectionSerializer,
    ShelfSerializer,
    StaffSerializer,
    TeacherSerializer,
)
from apps.academic.models import (
    Department,
    Grade,
    LibrarySection,
    Shelf,
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


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class StaffViewSet(ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
