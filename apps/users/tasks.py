from celery import shared_task

from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from core.LibraryMgmtSys.production import EMAIL_HOST_USER

User = get_user_model()


@shared_task
def send_mail_to_user(subject, message):
    from_email = EMAIL_HOST_USER

    # Get all users
    users = User.objects.filter()
    reciepent_list = [user.email for user in users]
    send_mail(subject, message, from_email, reciepent_list, fail_silently=False)
