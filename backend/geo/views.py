import re

import coreapi
import coreschema
import pytz
from rest_framework import mixins, schemas
from rest_framework import response
from rest_framework import status
from rest_framework import views
from rest_framework import viewsets

from geo import filters
from geo import models
from geo import serializers
from geo import utils


class CountryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Country.objects.order_by('name')
    serializer_class = serializers.CountrySerializer


class CityViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.City.objects.order_by('name')
    serializer_class = serializers.CitySerializer
    filterset_class = filters.CityFilterSet


class StateViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.State.objects.order_by('name')
    serializer_class = serializers.StateSerializer
    filter_fields = {
        'country_id': ['exact'],
        'name': ['icontains']
    }


class ZipViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.ZipSerializer
    search_fields = ('code',)

    def get_queryset(self):
        city_id = self.kwargs.get('pk')
        return models.Zip.objects.filter(city_id=city_id)


class LocationView(views.APIView):

    def get(self, request, *args, **kwargs):
        """
        View different locations for location search autocomplete.
        Example Url:\n
        api/v1/locations/?search=alabA
        Example JSON response:\n
            [
                {
                    "name": "Alabaster",
                    "_type": "City",
                    "_type_id": 2,
                    "_state_id": ""
                },
                {
                    "name": "Calabasas",
                    "_type": "City",
                    "_type_id": 2,
                    "_state_id": ""
                },
                {
                    "name": "Calabash",
                    "_type": "City",
                    "_type_id": 2,
                    "_state_id": ""
                },
                {
                    "name": "Malabar",
                    "_type": "City",
                    "_type_id": 2,
                    "_state_id": ""
                },
                {
                    "name": "Alabama",
                    "_type": "State",
                    "_type_id": 3,
                    "_state_id": "AL"
                }
            ]
        """
        search_param = request.query_params.get('search')
        query = utils.get_locations(search_param)
        return response.Response(
            data=list(query),
            status=status.HTTP_200_OK)


class TimezoneViewSet(views.APIView):

    """
    get:
        Returns timezones dictionary.
        Filtration by name is available
    """
    schema = schemas.ManualSchema(fields=[
        coreapi.Field(
            'name',
            required=False,
            location='query',
            schema=coreschema.String(
                description=(
                    'timezone name'
                )
            )
        ),
    ])

    @staticmethod
    def _get_timezone_keys(name=None):
        timezones = pytz.all_timezones
        if name:
            timezones = list(filter(
                lambda x: re.search(name, x.replace('_', ' '), re.IGNORECASE),
                timezones
            ))
        return timezones

    def get(self, request, *args, **kwargs):
        name_filter = request.query_params.get('name')
        timezone_keys = self._get_timezone_keys(name_filter)
        timezone_values = map(lambda x: x.replace('_', ' '), timezone_keys)
        timezones = dict(zip(timezone_keys, timezone_values))
        return response.Response(data=timezones)
