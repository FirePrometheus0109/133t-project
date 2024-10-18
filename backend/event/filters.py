import calendar
import datetime

import pytz
from django.db import models as orm
from django_filters import rest_framework as drf_filters

from event import models


class EventFilterSet(drf_filters.FilterSet):

    day = drf_filters.DateFilter(method='filter_day')
    month = drf_filters.DateFilter(method='filter_month')
    is_owner = drf_filters.BooleanFilter(method='filter_is_owner')

    def filter_month(self, queryset, name, value):  # noqa
        if value:
            date_from, date_to = self._get_month_period(value)
            return queryset.filter(
                orm.Q(time_from__range=[date_from, date_to])
                |
                orm.Q(time_to__range=[date_from, date_to]))
        return queryset

    def filter_day(self, queryset, name, value):  # noqa
        if value:
            date_from, date_to = self._get_day_period(value)
            return queryset.filter(
                orm.Q(time_from__range=[date_from, date_to])
                |
                orm.Q(time_to__range=[date_from, date_to]))
        return queryset

    def filter_is_owner(self, queryset, name, value):  # noqa
        if value:
            return queryset.filter(owner=self.request.user)
        return queryset

    def _get_day_period(self, date):
        tz_name = self.request.query_params.get('tz')
        tz = pytz.timezone(tz_name)
        date_start = datetime.datetime.combine(
            date,
            datetime.datetime.min.time()
        )
        date_end = datetime.datetime.combine(
            date,
            datetime.datetime.max.time()
        )
        date_start = tz.localize(date_start)
        date_end = tz.localize(date_end)
        return date_start.astimezone(pytz.utc), date_end.astimezone(pytz.utc)

    def _get_month_period(self, date):
        tz_name = self.request.query_params.get('tz')
        tz = pytz.timezone(tz_name)
        first_date_month = datetime.date(date.year, date.month, 1)
        last_date_month = datetime.date(
            date.year,
            date.month,
            calendar.monthrange(date.year, date.month)[1]
        )
        date_start = datetime.datetime.combine(
            first_date_month,
            datetime.datetime.min.time()
        )
        date_end = datetime.datetime.combine(
            last_date_month,
            datetime.datetime.max.time()
        )
        date_start = tz.localize(date_start)
        date_end = tz.localize(date_end)
        return date_start.astimezone(pytz.utc), date_end.astimezone(pytz.utc)

    class Meta:
        model = models.Event
        fields = (
            'type',
        )
