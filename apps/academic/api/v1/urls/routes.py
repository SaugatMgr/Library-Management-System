from rest_framework.routers import DefaultRouter

from apps.academic.api.v1.views.viewsets import (
    DepartmentViewSet,
    GradeViewSet,
    LibrarySectionViewSet,
    ShelfViewSet,
    TeacherViewSet,
    StaffViewSet,
)

academics_router = DefaultRouter()

academics_router.register("grades", GradeViewSet, basename="grades")
academics_router.register("departments", DepartmentViewSet, basename="departments")
academics_router.register(
    "library-sections", LibrarySectionViewSet, basename="library-sections"
)
academics_router.register("shelves", ShelfViewSet, basename="shelves")
academics_router.register("teachers", TeacherViewSet, basename="teachers")
academics_router.register("staffs", StaffViewSet, basename="staffs")
