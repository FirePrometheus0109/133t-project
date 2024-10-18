from rest_framework import pagination


class CandidateQuickViewPagination(pagination.LimitOffsetPagination):
    default_limit = 1
    max_limit = 1
