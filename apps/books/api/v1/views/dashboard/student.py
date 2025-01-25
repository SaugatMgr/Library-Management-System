from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Sum

from apps.books.models import Borrow, FinePayment
from utils.constants import BorrowStatusChoices


class StudentDashboard(APIView):
    http_method_names = ["get"]

    def get(self, request):
        current_user = request.user
        total_fine_paid = FinePayment.objects.filter(
            borrow__borrower=current_user
        ).aggregate(total_fine_paid=Sum("amount"))["total_fine_paid"]
        pending_book_returns = Borrow.objects.filter(
            borrower=current_user, borrow_status=BorrowStatusChoices.NOT_RETURNED
        ).count()
        overdue_books = Borrow.objects.filter(
            borrower=current_user,
            borrow_status=BorrowStatusChoices.NOT_RETURNED,
            overdue=True,
        ).count()

        return Response(
            {
                "user_name": current_user.get_full_name,
                "total_books_borrowed": current_user.borrow_set.count(),
                "total_fine_paid": total_fine_paid,
                "overdue_books": overdue_books,
                "pending_book_returns": pending_book_returns,
            }
        )
