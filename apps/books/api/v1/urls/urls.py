from django.urls import path

from apps.books.api.v1.views.dashboard.admin_dashboard import AdminDashboard
from apps.books.api.v1.views.dashboard.student import StudentDashboard
from apps.books.api.v1.views.report import ExportDataView

urlpatterns = [
    path("dashboard/admin/", AdminDashboard.as_view(), name="admin-dashboard"),
    path("dashboard/student/", StudentDashboard.as_view(), name="student-dashboard"),
    path("export/", ExportDataView.as_view(), name="export-data"),
]
