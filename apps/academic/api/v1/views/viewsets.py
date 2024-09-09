from rest_framework.viewsets import ModelViewSet

from apps.academic.api.v1.serializers.general import (
    DepartmentSerializer,
    GradeSerializer,
)
from apps.academic.models import (
    Department,
    Grade,
)


class GradeViewSet(ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer


class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
