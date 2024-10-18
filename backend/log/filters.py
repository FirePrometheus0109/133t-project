from django_filters import rest_framework as drf_filters

from log import models


class LogFilterSet(drf_filters.FilterSet):
    ct_model = drf_filters.CharFilter(method='filter_ct_model')

    @staticmethod
    def filter_ct_model(queryset, name, value):  # noqa
        """Filter log queryset by content type model."""
        if value:
            return queryset.filter(content_type__model=value)
        return queryset

    class Meta:
        model = models.Log
        fields = (
            'ct_model',
            'object_id'
        )
