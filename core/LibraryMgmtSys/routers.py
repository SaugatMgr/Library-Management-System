from rest_framework.routers import DefaultRouter

from apps.users.api.v1.urls.routes import user_router
from apps.books.api.v1.urls.routes import book_router
from apps.digital_resources.api.v1.urls.routes import digital_resources_router
from apps.academic.api.v1.urls.routes import academics_router
from apps.membership.api.v1.urls.routes import membership_router

# All apps router here
base_router = DefaultRouter()

base_router.registry.extend(user_router.registry)
base_router.registry.extend(book_router.registry)
base_router.registry.extend(digital_resources_router.registry)
base_router.registry.extend(academics_router.registry)
base_router.registry.extend(membership_router.registry)
