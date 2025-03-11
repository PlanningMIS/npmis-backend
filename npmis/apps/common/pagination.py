from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    """
    Extends the default PageNumberPagination from Django rest framework.
    This will generate a custom response that includes the pagination metadata.
    """
    def get_paginated_response(self, data):
        return Response({
            'status_code': status.HTTP_200_OK,
            'count': self.page.paginator.count,
            'page_size': self.get_page_size(self.request),
            'page_number': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'data': data,
        }, status=status.HTTP_200_OK)