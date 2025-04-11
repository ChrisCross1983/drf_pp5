from rest_framework.pagination import PageNumberPagination

class CommentPagination(PageNumberPagination):
    page_size = 10  # oder was du möchtest
    page_size_query_param = 'page_size'
    max_page_size = 100
