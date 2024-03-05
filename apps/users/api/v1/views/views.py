from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.api.v1.serializers.post import UserRegisterSerializer
from apps.users.models import CustomUser


class UserRegisterView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        user_register_serializer = UserRegisterSerializer(data=request.data)
        user_register_serializer.is_valid(raise_exception=True)
        validated_data = user_register_serializer.validated_data
        CustomUser.objects.create_user(**validated_data)
        return Response({"message": "User Registered Successfully."})
