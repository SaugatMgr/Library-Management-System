from rest_framework.viewsets import ModelViewSet

from apps.academic.api.v1.serializers.general import (
    DepartmentSerializer,
    GradeSerializer,
    TeacherSerializer,
)
from apps.academic.models import (
    Department,
    Grade,
    Teacher,
)


class GradeViewSet(ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer


class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
