from celery import shared_task

from django.core.mail import send_mail
from django.conf import settings

from apps.books.models import Book
from apps.users.models import CustomUser
from utils.helpers import get_instance_by_attr


@shared_task
def notify_book_available(user_id, book_id):
    user = get_instance_by_attr(CustomUser, "id", user_id)
    book = get_instance_by_attr(Book, "id", book_id)

    subject = "Book Now Available"
    message = f"Book {book.title} is available for you to borrow."
    from_email = settings.EMAIL_HOST_USER
    reciepent_list = [user.email]

    send_mail(subject, message, from_email, reciepent_list, fail_silently=False)
