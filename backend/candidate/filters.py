# pylint: disable=no-member,unused-argument
import datetime

from django.utils import timezone
from django_filters import rest_framework as dj_filters

from candidate import models
from leet import enums
from leet import filters as base_filters


def filter_candidates_by_yesterday(qs):
    yesterday_date = timezone.now().date() - datetime.timedelta(days=1)
    qs = qs.filter(applied_date__date=yesterday_date)
    return qs


def filter_candidates_by_this_week(qs):
    current_week_number = timezone.now().isocalendar()[1]
    qs = qs.filter(applied_date__week=current_week_number)
    return qs


def filter_candidates_by_last_week(qs):
    day_of_previous_week = timezone.now() - datetime.timedelta(days=7)
    previous_week_number = day_of_previous_week.isocalendar()[1]
    qs = qs.filter(applied_date__week=previous_week_number)
    return qs


def filter_candidates_by_this_month(qs):
    current_month = timezone.now().month
    qs = qs.filter(applied_date__month=current_month)
    return qs


def filter_candidates_by_last_month(qs):
    previous_month = timezone.now().month - 1
    qs = qs.filter(applied_date__month=previous_month)
    return qs


def filter_candidates_by_this_year(qs):
    current_year = timezone.now().year
    qs = qs.filter(applied_date__year=current_year)
    return qs


def filter_candidates_by_last_year(qs):
    previous_year = timezone.now().year - 1
    qs = qs.filter(applied_date__year=previous_year)
    return qs


FILTER_CANDIDATE_BY_DATE_METHODS = {
    enums.AppliedDateFilterEnum.YESTERDAY.name:
        filter_candidates_by_yesterday,
    enums.AppliedDateFilterEnum.THIS_WEEK.name:
        filter_candidates_by_this_week,
    enums.AppliedDateFilterEnum.LAST_WEEK.name:
        filter_candidates_by_last_week,
    enums.AppliedDateFilterEnum.THIS_MONTH.name:
        filter_candidates_by_this_month,
    enums.AppliedDateFilterEnum.LAST_MONTH.name:
        filter_candidates_by_last_month,
    enums.AppliedDateFilterEnum.THIS_YEAR.name:
        filter_candidates_by_this_year,
    enums.AppliedDateFilterEnum.LAST_YEAR.name:
        filter_candidates_by_last_year,
}


ENUM_NUM_DAYS_MAP = {
    enums.WorkflowStepsCompanyStatFilters.TWO_WEEKS.name: 14,
    enums.WorkflowStepsCompanyStatFilters.THIRTY_DAYS.name: 30,
    enums.WorkflowStepsCompanyStatFilters.SIXTY_DAYS.name: 60,
}


class FilterLocationFilterSet(base_filters.FilterLocationFilterSet):

    search_vector_field = 'job_seeker__location_search_vector'


class CandidateFilterSet(FilterLocationFilterSet):
    applied_date = dj_filters.ChoiceFilter(
        choices=enums.AppliedDateFilterEnum.choices,
        method='filter_applied_date'
    )
    rating__rating = dj_filters.ChoiceFilter(
        choices=enums.RatingEnum.choices,
        null_value=enums.RatingEnum.NO_RATING.name
    )

    class Meta:
        model = models.Candidate
        fields = (
            'applied_date',
            'rating__rating',
            'job_seeker__address__city__id',
            'status',
        )

    @staticmethod
    def filter_applied_date(queryset, name, value):
        return FILTER_CANDIDATE_BY_DATE_METHODS[value](queryset)


class CompanyReportFilterSet(dj_filters.FilterSet):
    from_date = dj_filters.IsoDateTimeFilter(
        method=lambda qs, name, value: qs,
        required=True,
    )
    to_date = dj_filters.IsoDateTimeFilter(
        method='filter_date_range',
        required=True,
    )

    def filter_date_range(self, queryset, name, value):
        from_date = self.data.get('from_date')
        to_date = self.data.get(name)
        return queryset.filter(created_at__range=(from_date, to_date))

    class Meta:
        model = models.WorkflowStep
        fields = (
            'from_date',
            'to_date'
        )


class WorkflowStepsFilterSet(dj_filters.FilterSet):
    created_at = dj_filters.ChoiceFilter(
        choices=enums.WorkflowStepsCompanyStatFilters.choices,
        method='filter_created_at',
    )

    @staticmethod
    def filter_created_at(queryset, name, value):
        number_days = ENUM_NUM_DAYS_MAP[value]
        filter_date = timezone.now() - datetime.timedelta(days=number_days)
        queryset = queryset.filter(created_at__gte=filter_date)
        return queryset


class FullTextSearchBackend(base_filters.FullTextSearchBackend):

    search_title = 'Full text search.'
    search_description = 'Full text search for list of candidates.'
    search_vector_field = 'job_seeker__search_vector'
