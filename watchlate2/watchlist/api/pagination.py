from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class WatchListPagination(PageNumberPagination):
    # number of items per page
    page_size = 3
    # the name of the parameter
    page_query_param = 'p'
    # allowing the user to choose the number of items per page
    page_size_query_param = 'size'
    # to give the max value that the user cannot pass
    max_page_size = 7
    # to access the last page
    last_page_strings = ['end', ]


class WatchListLO(LimitOffsetPagination):
    # the number of items in a page
    default_limit = 3
    # limit the number of items in a request
    max_limit = 6
    # rename the limit in url
    limit_query_param = 'limit'
    # rename the offset
    offset_query_param = 'start'


class WatchListCursor(CursorPagination):
    # cursor only to pass page by page
    # number of items
    page_size = 3
    # by default -created the newest to oldest
    ordering = "avg_rating"
    # rename the cursor
    cursor_query_param = 'record'
