from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.api.v1.auth import CustomTokenObtainPairView, CustomTokenVerifyView
from apps.users.api.v1.views.views import (
    ChangePasswordView,
    PasswordResetRequestView,
    ResetPasswordView,
    UserEmailVerificationView,
    UserRegisterView,
    schedule_mail_celery,
    send_mail_celery,
)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("verify-email/", UserEmailVerificationView.as_view(), name="verify_email"),
    path("send-mail/", send_mail_celery, name="send_mail"),
    path("schedule-mail/", schedule_mail_celery, name="schedule_mail"),
    path(
        "account/password/change/", ChangePasswordView.as_view(), name="change_password"
    ),
    path(
        "account/password/email/",
        PasswordResetRequestView.as_view(),
        name="reset_password_request)",
    ),
    path("account/password/reset/", ResetPasswordView.as_view(), name="reset_password"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", CustomTokenVerifyView.as_view(), name="token_verify"),
]
