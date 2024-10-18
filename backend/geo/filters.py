from django_filters.rest_framework import filterset, filters

from geo.models import City


class CityFilterSet(filterset.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    state_id = filters.NumberFilter(field_name='state_id')
    country_id = filters.NumberFilter(field_name='state__country_id')

    class Meta:
        model = City
        fields = ('name', 'state_id', 'country_id')
