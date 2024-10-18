# pylint: disable=unused-argument
import datetime

from django.utils import timezone
from django_filters import rest_framework as drf_filters
from rest_framework import filters as filter_backends

from job_seeker import models
from leet import filters as base_filters


class JobSeekerFilterSet(base_filters.FilterLocationFilterSet):
    """Custom filterset backend for list of job seekers."""

    # TODO (i.bogretsov) discuss with front-end about long naming
    position_type = drf_filters.Filter(method='filter_position_type')
    clearance = drf_filters.Filter(method='filter_clearance')
    profile_updated_within_days = drf_filters.NumberFilter(
        method='filter_profile_updated_within_days')
    skills = drf_filters.NumberFilter(method='filter_skills')
    saved = drf_filters.BooleanFilter(method='filter_saved')
    purchased = drf_filters.BooleanFilter(method='filter_purchased')

    def filter_position_type(self, queryset, name, value):
        # TODO (i.bogretsov) add other behaviour
        value = self.data.getlist(name)
        return queryset.filter(position_type__in=value)

    def filter_clearance(self, queryset, name, value):
        value = self.data.getlist(name)
        return queryset.filter(clearance__in=value)

    def filter_skills(self, queryset, name, value):
        value = self.data.getlist(name)
        return queryset.filter(skills__id__in=value)

    @staticmethod
    def filter_profile_updated_within_days(queryset, name, value):
        today = timezone.now()
        last_updated_date = today - datetime.timedelta(days=int(value))
        return queryset.filter(modified_at__date__gte=last_updated_date.date())

    def filter_saved(self, queryset, name, value):  # noqa
        if value:
            return queryset.filter(
                savedjobseeker__company_user__user=self.request.user)
        return queryset

    def filter_purchased(self, queryset, name, value):  # noqa
        if value:
            purchased_ids = (self.request.user
                             .company_user
                             .company
                             .purchased_job_seekers
                             .values_list('id', flat=True))
            return queryset.filter(id__in=purchased_ids)
        return queryset

    class Meta:
        model = models.JobSeeker
        fields = (
            'experience',
            'education',
            'travel',
        )


class FullTextSearchBackend(base_filters.FullTextSearchBackend):

    search_title = 'Full text search.'
    search_description = 'Full text search for list of job seekers.'


class JobSeekerListOrderingFilterBackend(filter_backends.OrderingFilter):

    ordering_map = {
        'rank': (
            '-rank',
            '-modified_at'
        ),
        'modified_at': (
            '-modified_at',
            '-rank'
        ),
        'first_name': (
            '-user__first_name',
        ),
        'last_name': (
            '-user__last_name',
        )
    }

    def filter_queryset(self, request, queryset, view):
        """Order result job seeker queryset after filtering and searching."""
        param = request.query_params.get(self.ordering_param, 'rank')
        if not queryset:
            return queryset
        queryset = queryset.order_by(*self.ordering_map[param])
        if queryset and hasattr(queryset[0], 'loca_rank'):
            queryset = queryset.order_by('-loca_rank')
        return queryset
