from rest_framework import pagination


class StandardResultPagination(pagination.PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'


class BulkResultPagination(pagination.PageNumberPagination):
    page_size = 3000
    page_size_query_param = 'page_size'