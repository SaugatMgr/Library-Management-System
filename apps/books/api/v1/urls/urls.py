from django.urls import path

from apps.books.api.v1.views.admin_dashboard import AdminDashboard

urlpatterns = [
    path("dashboard/admin/", AdminDashboard.as_view(), name="admin-dashboard"),
]
