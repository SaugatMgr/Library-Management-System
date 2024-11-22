from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from django.db.models import Count
from django.utils import timezone

from apps.academic.models import Staff, Student
from apps.books.models import Borrow
from utils.constants import BorrowStatusChoices


class AdminDashboard(APIView):
    http_method_names = ["get"]
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_students = Student.objects.count()
        total_staff = Staff.objects.count()
        pending_book_returns = Borrow.objects.filter(
            borrow_status=BorrowStatusChoices.NOT_RETURNED
        ).count()
        overdue_books = Borrow.objects.filter(
            borrow_status=BorrowStatusChoices.NOT_RETURNED, due_date__lt=timezone.now()
        ).count()
        most_borrowed_books = (
            Borrow.objects.values("book__title")
            .annotate(borrow_count=Count("book"))
            .order_by("-borrow_count")
        )

        return Response(
            {
                "total_students": total_students,
                "total_staff": total_staff,
                "overdue_books": overdue_books,
                "pending_book_returns": pending_book_returns,
                "most_borrowed_books": most_borrowed_books,
            }
        )
