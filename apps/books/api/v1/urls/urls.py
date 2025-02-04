from django.urls import path

from apps.books.api.v1.views.dashboard.admin_dashboard import (
    AdminDashboard,
    MostBorrowedBooks,
    PendingBooks,
)
from apps.books.api.v1.views.dashboard.student import StudentDashboard
from apps.books.api.v1.views.report import ExportDataView

urlpatterns = [
    path("dashboard/admin/", AdminDashboard.as_view(), name="admin-dashboard"),
    path("dashboard/student/", StudentDashboard.as_view(), name="student-dashboard"),
    path("export-data/", ExportDataView.as_view(), name="export-data"),
    path(
        "most-borrowed-books/", MostBorrowedBooks.as_view(), name="most-borrowed-books"
    ),
    path("pending-books/", PendingBooks.as_view(), name="pending-books"),
    path("overdue-books/", PendingBooks.as_view(), name="overdue-books"),
]
