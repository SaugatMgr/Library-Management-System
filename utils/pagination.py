import math
from rest_framework import pagination
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.pagination import InvalidPage


class CustomPageSizePagination(pagination.PageNumberPagination):
    PAGE_SIZE = 10

    def paginate_queryset(self, queryset, request, view=None):
        page_size_param = request.query_params.get("per_page")
        query_count = queryset.count()
        if page_size_param == "all":
            # Return all data if per_page is "all"
            if query_count == 0:
                self.page_size = self.PAGE_SIZE
            else:
                self.page_size = queryset.count()
        else:
            self.page_size = int(page_size_param) if page_size_param else self.PAGE_SIZE

        page_number = request.query_params.get(self.page_query_param, 1)
        paginator = self.django_paginator_class(queryset, self.page_size)

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):
        per_page = self.request.query_params.get("per_page", self.PAGE_SIZE)

        if per_page == "all":
            # If per_page is "all", return all data in the specified format
            return Response(
                {
                    "current_page": 1,
                    "total": self.page.paginator.count,
                    "per_page": "all",
                    "total_pages": 1,
                    "results": data,
                }
            )

        total_pages_count = math.ceil(self.page.paginator.count / int(per_page))
        return Response(
            {
                "current_page": int(self.request.query_params.get("page", 1)),
                "total": self.page.paginator.count,
                "per_page": int(per_page),
                "total_pages": total_pages_count,
                "results": data,
            }
        )
