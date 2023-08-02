from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """Кастомный паджинатор с учетом параметра `limit`."""
    page_size_query_param = 'limit'
