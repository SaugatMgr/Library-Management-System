import pandas as pd
import ast
import requests
import os
import mimetypes

from urllib.parse import urlparse
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from decimal import InvalidOperation
from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from django.utils import timezone

from django.core.files.base import ContentFile
from apps.books.models import Book, Genre
from utils.helpers import generate_unique_file_name


def parse_date(date_str):
    formats = ["%m/%d/%Y", "%m/%d/%y", "%d-%m-%Y", "%d-%m-%y"]
    for fmt in formats:
        try:
            naive_datetime = datetime.strptime(date_str, fmt)
            return timezone.make_aware(naive_datetime, timezone.get_current_timezone())
        except ValueError:
            continue
    print(f"Date format for '{date_str}' not recognized.")
    return None


class Command(BaseCommand):
    help = "Import book data from a CSV file to the database"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("file_path", type=str, help="Path to the CSV file")

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            file_path = kwargs["file_path"]
            df = pd.read_csv(file_path)
            new_df = df.dropna(
                subset=[
                    "title",
                    "author",
                    "description",
                    "isbn",
                    "genres",
                    "pages",
                    "publisher",
                    "publishDate",
                    "coverImg",
                    "price",
                ]
            )
            for index, row in new_df.head(70).iterrows():
                book_data = {
                    "title": row["title"],
                    "author": row["author"],
                    "publisher": row["publisher"],
                    "publication_date": row["publishDate"],
                    "description": row["description"],
                    "pages": row["pages"],
                    "price": row["price"],
                    "isbn": row["isbn"],
                    "genres": ast.literal_eval(row["genres"]),
                    "cover_url": row["coverImg"],
                }
                self.save_book_with_image(book_data)

    def save_book_with_image(self, book_data):
        publication_date = book_data.pop("publication_date")
        genres = book_data.pop("genres")
        price_str = book_data.pop("price")

        try:
            dec_price_val = Decimal(price_str) * Decimal("134.20")
            formatted_price_value = dec_price_val.quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
        except (InvalidOperation, ValueError) as e:
            print(f"Error converting price: {e}")

        cover_url = book_data.pop("cover_url")
        book_data["publication_date"] = parse_date(publication_date)
        book_data["pages"] = int(book_data["pages"])
        book_data["price"] = formatted_price_value
        book_data["quantity"] = 1

        try:
            response = requests.get(cover_url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching image: {e}")
            return

        image_data = response.content

        parsed_url = urlparse(cover_url)
        _, file_extension = os.path.splitext(os.path.basename(parsed_url.path))
        if not file_extension:
            file_extension = mimetypes.guess_extension(
                response.headers.get("Content-Type", "image/jpeg")
            )

        image_file_name = generate_unique_file_name(cover=True)
        full_file_name = f"{image_file_name}{file_extension}"

        image_file = ContentFile(image_data, name=full_file_name)

        book = Book(**book_data)
        book.save()
        book.cover.save(full_file_name, image_file, save=True)

        genre_objects = [
            Genre(name=genre_name)
            for genre_name in genres
            if Genre.objects.filter(name=genre_name).exists() is False
        ]
        Genre.objects.bulk_create(genre_objects)

        created_genres = Genre.objects.filter(name__in=genres)
        book.genres.set(created_genres)
        self.stdout.write(
            self.style.SUCCESS(f"Successfully imported book: {book.title}")
        )
