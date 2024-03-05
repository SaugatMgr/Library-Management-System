from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.api.v1.auth import CustomTokenObtainPairView, CustomTokenVerifyView
from apps.users.api.v1.views.views import UserRegisterView

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", CustomTokenVerifyView.as_view(), name="token_verify"),
]
