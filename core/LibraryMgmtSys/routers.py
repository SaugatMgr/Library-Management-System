from rest_framework.routers import DefaultRouter

from apps.users.api.v1.urls.routes import user_router
from apps.books.api.v1.urls.routes import book_router

# All apps router here
base_router = DefaultRouter()

base_router.registry.extend(user_router.registry)
base_router.registry.extend(book_router.registry)
