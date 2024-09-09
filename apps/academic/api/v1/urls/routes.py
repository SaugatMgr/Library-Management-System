from rest_framework.routers import DefaultRouter

from apps.academic.api.v1.views.viewsets import (
    DepartmentViewSet,
    GradeViewSet,
)

academics_router = DefaultRouter()

academics_router.register("grades", GradeViewSet, basename="grades")
academics_router.register("departments", DepartmentViewSet, basename="departments")
