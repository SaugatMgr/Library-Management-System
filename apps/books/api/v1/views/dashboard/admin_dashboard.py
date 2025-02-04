from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from django.db.models import Count, Exists, OuterRef
from django.utils import timezone

from apps.academic.models import Staff, Student
from apps.books.api.v1.serializers.get import BookListDetailSerializer
from apps.books.models import Book, Borrow
from utils.constants import BorrowStatusChoices
from utils.pagination import CustomPageSizePagination
from utils.permissions import LibrarianOrAdminPermission


class AdminDashboard(APIView):
    http_method_names = ["get"]
    permission_classes = [LibrarianOrAdminPermission]

    def get(self, request):
        total_students = Student.objects.count()
        total_staff = Staff.objects.count()
        pending_book_returns = Borrow.objects.filter(
            borrow_status=BorrowStatusChoices.NOT_RETURNED
        ).count()
        overdue_books = Borrow.objects.filter(
            borrow_status=BorrowStatusChoices.NOT_RETURNED, due_date__lt=timezone.now()
        ).count()

        return Response(
            {
                "total_students": total_students,
                "total_staff": total_staff,
                "overdue_books": overdue_books,
                "pending_book_returns": pending_book_returns,
            }
        )


class OverDueBooks(ListAPIView):
    serializer_class = BookListDetailSerializer
    permission_classes = [LibrarianOrAdminPermission]
    pagination_class = CustomPageSizePagination

    def get_queryset(self):
        return Book.objects.filter(
            Exists(
                Borrow.objects.filter(
                    book=OuterRef("id"),
                    borrow_status=BorrowStatusChoices.NOT_RETURNED,
                    due_date__lt=timezone.now(),
                )
            )
        )


class MostBorrowedBooks(ListAPIView):
    serializer_class = BookListDetailSerializer
    permission_classes = [LibrarianOrAdminPermission]
    pagination_class = CustomPageSizePagination

    def get_queryset(self):
        queryset = (
            Book.objects.annotate(borrow_count=Count("borrow"))
            .filter(borrow_count__gt=0)
            .order_by("-borrow_count")
        )
        return queryset


class PendingBooks(ListAPIView):
    serializer_class = BookListDetailSerializer
    permission_classes = [LibrarianOrAdminPermission]
    pagination_class = CustomPageSizePagination

    def get_queryset(self):
        return Book.objects.filter(
            Exists(
                Borrow.objects.filter(
                    book=OuterRef("id"),
                    borrow_status=BorrowStatusChoices.NOT_RETURNED,
                )
            )
        )
