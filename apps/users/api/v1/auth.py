from rest_framework.request import Request
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework.response import Response
from apps.users.api.v1.serializers.get import UserListSerializer
from apps.users.api.v1.serializers.post import (
    CustomTokenObtainPairSerializer,
    CustomTokenVerifySerializer,
)
from apps.users.models import CustomUser


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        token_serializer = self.get_serializer(data=request.data)
        token_serializer.is_valid(raise_exception=True)
        validated_data = token_serializer.validated_data
        response = {
            "token": validated_data,
            "user": UserListSerializer(validated_data.pop("user")).data,
        }
        return Response(response)


class CustomTokenVerifyView(TokenVerifyView):
    serializer_class = CustomTokenVerifySerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        try:
            data = request.data
            token_verify_serializer = self.get_serializer(data=data)
            token_verify_serializer.is_valid(raise_exception=True)
            decoded_token = AccessToken(token=data["token"])
            user = CustomUser.objects.get(id=decoded_token.payload["user_id"])
            refresh_token = RefreshToken.for_user(user)
            response = {
                "token": {
                    "access": str(decoded_token),
                    "refresh": str(refresh_token),
                    "access_expires_on": api_settings.ACCESS_TOKEN_LIFETIME,
                    "refresh_expires_on": api_settings.REFRESH_TOKEN_LIFETIME,
                },
                "user": UserListSerializer(user).data,
            }
            return Response(response)
        except Exception as e:
            return Response(
                {"error": str(e), "field": "access"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
