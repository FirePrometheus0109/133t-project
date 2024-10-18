import functools
import operator

import coreapi
import coreschema
from django.contrib.postgres import search
from django.db import models as orm
from django.utils import encoding
from django_filters import rest_framework as drf_filters
from rest_framework import filters as filter_backends
from rest_framework.settings import api_settings

from leet import constants


class FilterLocationFilterSet(drf_filters.FilterSet):
    """
    FilterSet for full text search by location.
    This filterset is used for inheritance by childrens filtersets.
    """

    location = drf_filters.Filter(method='filter_location')
    search_vector_field = 'location_search_vector'

    def filter_location(self, queryset, name, value):  # noqa
        values = self.data.getlist('location', [])
        clauses = (search.SearchQuery(v) for v in values)
        query = functools.reduce(operator.or_, clauses)
        queryset = (queryset
                    .annotate(loca_rank=search.SearchRank(
                        orm.F(self.search_vector_field),
                        query))
                    .filter(
                        loca_rank__gt=constants.MIN_FULL_TEXT_SEARCH_WEIGHT))
        return queryset


class FullTextSearchBackend(filter_backends.BaseFilterBackend):

    search_param = api_settings.SEARCH_PARAM
    search_title = ''
    search_description = ''
    search_vector_field = 'search_vector'

    def filter_queryset(self, request, queryset, view):
        """Full text search."""
        value = request.query_params.get(self.search_param, '')
        values = self.parse_fts_params(value)
        if not values:
            return queryset
        clauses = (search.SearchQuery(v) for v in values)
        query = functools.reduce(operator.or_, clauses)
        queryset = (queryset
                    .annotate(rank=search.SearchRank(
                        orm.F(self.search_vector_field),
                        query))
                    .filter(rank__gt=constants.MIN_FULL_TEXT_SEARCH_WEIGHT))
        return queryset

    @staticmethod
    def parse_fts_params(params):
        replaced_chars = [',', ';', '.']
        for ch in replaced_chars:
            params = params.replace(ch, ' ')
        return [i for i in params.split(' ') if i]

    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='search',
                required=False,
                location='query',
                schema=coreschema.String(
                    title=encoding.force_text(self.search_title),
                    description=encoding.force_text(self.search_description)
                )
            )
        ]
