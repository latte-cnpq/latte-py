from django.conf import settings
from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        next_page_number = (
            self.page.next_page_number() if self.page.has_next() else None
        )

        return Response(
            {
                "next": next_page_number,
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "results": data,
            }
        )
