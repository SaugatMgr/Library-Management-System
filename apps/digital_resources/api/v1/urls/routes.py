from rest_framework.routers import DefaultRouter

from apps.digital_resources.api.v1.views.viewsets import (
    DigitalResourceModelViewSet,
)

digital_resources_router = DefaultRouter()

digital_resources_router.register(
    "digital-resources", DigitalResourceModelViewSet, basename="digital_resources"
)
