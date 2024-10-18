from django_filters import rest_framework as dj_filters
from rest_framework import filters as drf_filters

from candidate import filters
from candidate import models
from candidate import utils
from permission import permissions


class CompanyCandidateViewMixin:

    queryset = (models.Candidate.objects
                      .select_related(
                          'job',
                          'job_seeker',
                          'apply',
                          'apply__cover_letter')
                      .prefetch_related(
                          'rating',
                          'workflow_steps',
                          'workflow_steps__owner',
                          'workflow_steps__owner__user',
                          'job__answers__answer',
                          'job__job_skill_set',
                          'job_seeker__skills',
                          'job_seeker__user',
                          'job_seeker__answers',
                          'job_seeker__answers__answer',
                          'job_seeker__answers__question',
                          'job_seeker__answers__job'
                      ))
    permission_classes = (
        permissions.BaseModelPermissions,
        permissions.HasSubscription
    )

    def get_queryset(self):
        # TODO (i.bogretsov) move to managers,
        # because queryset is calculated two times
        qs = utils.annotate_candidates_qs_with_candidate_data(self.queryset)
        return qs.order_by('-applied_date')

    def filter_queryset(self, queryset):
        company = self.request.user.company_user.company
        queryset = queryset.filter(job__company=company)
        return super().filter_queryset(queryset)


class CompanyCandidateViewListMixin:

    filter_backends = (
        filters.FullTextSearchBackend,
        dj_filters.DjangoFilterBackend,
        drf_filters.OrderingFilter,
    )
    filterset_class = filters.CandidateFilterSet
    ordering_fields = (
        'job_seeker__user__first_name',
        'job_seeker__user__last_name',
        'job__title',
        'applied_date',
    )
