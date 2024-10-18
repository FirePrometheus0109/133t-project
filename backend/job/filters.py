import datetime

from django.conf import settings
from django.db import models as orm
from django.utils import timezone
from django_filters import rest_framework as drf_filters
from rest_framework import filters as filter_backends

from job import models
from leet import filters as leet_filters


class BaseJobFilterSet(leet_filters.FilterLocationFilterSet):
    state_id = drf_filters.NumberFilter(field_name='location__city__state_id')
    city_id = drf_filters.NumberFilter(field_name='location__city_id')
    clearance = drf_filters.Filter(method='filter_clearance')

    def filter_clearance(self, queryset, name, value):
        value = self.data.getlist(name)
        return queryset.filter(clearance__in=value)


class JobFilterSet(BaseJobFilterSet):
    """Custom filter backend for list of jobs."""

    owner = drf_filters.Filter(method='filter_owner')
    position_type = drf_filters.Filter(method='filter_position_type')
    skills = drf_filters.Filter(method='filter_skills')
    company = drf_filters.Filter(method='filter_company')
    excl_company = drf_filters.Filter(method='filter_excluded_company')
    salary = drf_filters.NumericRangeFilter(method='filter_salary')
    posted_ago = drf_filters.NumberFilter(
        method='filter_posted_ago')

    @staticmethod
    def filter_posted_ago(queryset, name, value):  # noqa
        today = timezone.now()
        ago = today - datetime.timedelta(days=int(value))
        return queryset.filter(publish_date__date__gte=ago.date())

    def filter_owner(self, queryset, name, value):  # noqa
        value = self.data.getlist(name)
        return queryset.filter(owner_id__in=value)

    def filter_position_type(self, queryset, name, value):
        value = self.data.getlist(name)
        return queryset.filter(position_type__in=value)

    def filter_skills(self, queryset, name, value):
        value = self.data.getlist(name)
        return queryset.filter(job_skill_set__skill__id__in=value)

    def filter_company(self, queryset, name, value):
        value = self.data.getlist(name)
        return queryset.filter(company__id__in=value)

    def filter_excluded_company(self, queryset, name, value):
        value = self.data.getlist(name)
        return queryset.exclude(company__id__in=value)

    def filter_salary(self, queryset, name, value):  # noqa
        salary_min = int(value.start) if value.start is not None else 0
        salary_max = settings.MAX_SALARY + 1

        if value.stop is not None:
            salary_max = int(value.stop)

        queryset = queryset.exclude(salary_negotiable=True)
        queryset = queryset.exclude(
            orm.Q(salary_min__gt=salary_max)
            |
            (
                orm.Q(salary_min__lt=salary_min)
                &
                orm.Q(salary_max__isnull=True)
            )
        )
        return queryset

    class Meta:
        model = models.Job
        fields = (
            'status',
            'owner',
            'is_deleted',
            'company_id',
            'state_id',
            'city_id',
            'education',
            'experience',
            'position_type',
            'clearance',
            'travel',
            'skills',
            'company',
            'excl_company',
            'location',
            'posted_ago',
            'salary',
        )


class FullTextSearchBackend(leet_filters.FullTextSearchBackend):

    search_title = 'Full text search.'
    search_description = 'Full text search for list of jobs.'


class JobListOrderingFilterBackend(filter_backends.OrderingFilter):

    ordering_map = {
        'rank': (
            '-rank',
            '-loca_rank',
            '-publish_date__date',
            '-matching_percent'
        ),
        'publish_date': (
            '-publish_date__date',
            '-matching_percent',
            '-rank',
            '-loca_rank'
        ),
        'matching_percent': (
            '-matching_percent',
            '-publish_date__date',
            '-rank',
            '-loca_rank'
        )
    }

    def filter_queryset(self, request, queryset, view):
        """Order result jobs queryset after filtering and searching."""
        param = request.query_params.get(self.ordering_param, 'rank')
        if param and queryset:
            queryset = queryset.order_by(*self.ordering_map[param])
        return queryset


class CompanyUserJobListOrderingFilterBackend(filter_backends.OrderingFilter):

    ordering_map = {
        'rank': (
            '-rank',
            '-loca_rank',
            '-publish_date__date',
        ),
        'publish_date': (
            '-publish_date__date',
            '-rank',
            '-loca_rank'
        )
    }
