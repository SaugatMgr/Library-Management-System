from django.db import transaction

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from apps.books.api.v1.repository import BookRepository
from apps.books.api.v1.serializers.get import (
    BookListDetailSerializer,
    GenreSerializer,
    TagSerializer,
)
from apps.books.api.v1.serializers.post import BookCreateUpdateSerializer
from apps.books.models import Genre, Tag
from utils.helpers import to_internal_value


class GenreModelViewSet(ModelViewSet):
    queryset = Genre.objects.filter()
    serializer_class = GenreSerializer


class TagModelViewSet(ModelViewSet):
    queryset = Tag.objects.filter()
    serializer_class = TagSerializer


class BookModelViewSet(ModelViewSet):
    serializer_action = {
        "list": BookListDetailSerializer,
        "retrieve": BookListDetailSerializer,
        "create": BookCreateUpdateSerializer,
        "update": BookCreateUpdateSerializer,
    }

    def get_queryset(self):
        return BookRepository.get_all()

    def get_serializer_class(self):
        return self.serializer_action.get(self.action)

    def create(self, request, *args, **kwargs):
        data = request.data
        cover = data.pop("cover")
        if cover:
            data["cover"] = to_internal_value(cover)
        book_serializer = self.get_serializer(data=data)
        book_serializer.is_valid(raise_exception=True)
        book_serializer.save()
        return Response({"message": "Book created successfully"}, status=201)

    def update(self, request, *args, **kwargs):
        data = request.data
        book_serializer = self.get_serializer(
            instance=self.get_object(), data=data, partial=True
        )
        book_serializer.is_valid(raise_exception=True)
        book_serializer.save()
        return Response({"message": "Book updated successfully."}, status=200)

    @action(detail=True, methods=["post"], url_path="borrow-book")
    def borrow_book(self, request, *args, **kwargs):
        with transaction.atomic():
            data = {
                "days": request.data["days"],
                "book_id": kwargs.get("pk"),
                "borrower": request.user,
            }
            BookRepository.borrow_book(data)
            return Response({"message": "Book borrowed successfully"})
