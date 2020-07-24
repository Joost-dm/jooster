""" Forum pagination classes. """

from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """ 10-units base pagination class. """

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 15
