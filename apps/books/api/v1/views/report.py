import pandas as pd

from io import BytesIO

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import HttpResponse

from apps.books.api.v1.serializers.get import ExportDataSerializer
from apps.books.models import Book


class ExportDataView(APIView):
    def post(self, request):
        serializer = ExportDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        books_id_list = validated_data["books_id_list"]
        file_format = validated_data["format"]
        fields = [
            "title",
            "author",
            "publisher",
            "publication_date",
            "description",
            "cover",
            "pages",
            "price",
            "quantity",
            "isbn",
            "availability_status",
        ]
        book_ids = [book.id for book in books_id_list]
        queryset = Book.objects.filter(id__in=book_ids)
        data = queryset.values(*fields)

        df = pd.DataFrame(data)
        df["publication_date"] = df["publication_date"].dt.tz_localize(None)

        if file_format == "csv":
            return self.generate_csv(df, fields)
        elif file_format == "excel":
            return self.generate_excel(df)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_csv(self, data, fields):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="export.csv"'
        data.to_csv(response, columns=fields, index=False, encoding="utf-8")
        return response

    def generate_excel(self, data):
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="export.xlsx"'
        with BytesIO() as buffer:
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                data.to_excel(writer, index=False)
            buffer.seek(0)
            response.write(buffer.read())
        return response
