from rest_framework.routers import DefaultRouter

from apps.books.api.v1.views.viewsets import (
    BookModelViewSet,
    GenreModelViewSet,
    TagModelViewSet,
)

book_router = DefaultRouter()

book_router.register("genres", GenreModelViewSet, basename="genres")
book_router.register("tags", TagModelViewSet, basename="tags")
book_router.register("books", BookModelViewSet, basename="books")
