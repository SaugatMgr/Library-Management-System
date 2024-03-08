from rest_framework.routers import DefaultRouter

from apps.users.api.v1.views.viewsets import UserProfileViewSet, UserViewset

user_router = DefaultRouter()

user_router.register("user", UserViewset, basename="user")
user_router.register("user-profile", UserProfileViewSet, basename="user-profile")
