# pylint: disable=no-self-use
from django.contrib import admin
from django.db import models as orm
from django.db.models import functions
from rangefilter import filter as range_filter

from job_seeker import models
from leet import admin as base_admin
from leet import enums
from leet import mixins


@admin.register(models.Education, site=base_admin.base_admin_site)
class EducationAdmin(mixins.AllowReadOnlyModelAdminMixin,
                     base_admin.BaseModelAdmin):
    pass


@admin.register(models.Certification, site=base_admin.base_admin_site)
class CertificationAdmin(mixins.AllowReadOnlyModelAdminMixin,
                         base_admin.BaseModelAdmin):
    pass


@admin.register(models.JobSeekerActivityReport,
                site=base_admin.base_admin_site)
class JobSeekerActivityReportsAdmin(
        mixins.ReportAdminMixin,
        mixins.AllowReadOnlyModelAdminMixin,
        admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'autoapplies_count',
        'applies_count',
        'manual_applies_count'
    )
    list_filter = (
        ('created_at', base_admin.AggregationsFilter),
    )
    csv_filename = 'JobSeekerActivityReport'

    def name(self, job_seeker):
        return job_seeker.user.get_full_name()
    name.short_description = 'Name'

    def email(self, job_seeker):
        return job_seeker.user.email
    email.short_description = 'Email'

    def autoapplies_count(self, job_seeker):
        return job_seeker.autoapplies_count

    autoapplies_count.short_description = 'Autoapplies Count'

    def applies_count(self, job_seeker):
        return job_seeker.applies_count

    applies_count.short_description = 'Applies Count'

    def manual_applies_count(self, job_seeker):
        return job_seeker.manual_applies_count
    manual_applies_count.short_description = 'Manual Applies Count'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        date_filters = self.get_date_filters(request.GET.dict())
        autoapplies_count_filter = {}
        applies_count_filter = {
            'applies__autoapply__isnull': False,
            'applies__status': enums.ApplyStatusEnum.APPLIED.name  # noqa
        }
        manual_applies_count_filter = {
            'applies__autoapply__isnull': True,
            'applies__status': enums.ApplyStatusEnum.APPLIED.name  # noqa
        }

        from_date = date_filters.get('created_at__gte')
        until_date = date_filters.get('created_at__lte')
        if from_date:
            autoapplies_count_filter.update(
                {'autoapplies__created_at__date__gte': from_date}
            )
            applies_count_filter.update(
                {'applies__applied_at__date__gte': from_date}
            )
            manual_applies_count_filter.update(
                {'applies__applied_at__date__gte': from_date}
            )
        if until_date:
            autoapplies_count_filter.update(
                {'autoapplies__created_at__date__lte': until_date}
            )
            applies_count_filter.update(
                {'applies__applied_at__date__lte': until_date}
            )
            manual_applies_count_filter.update(
                {'applies__applied_at__date__lte': until_date}
            )
        annotations = {
            'autoapplies_count': orm.Count(
                'autoapplies',
                filter=orm.Q(**autoapplies_count_filter),
                distinct=True
            ),
            'applies_count': orm.Count(
                'applies',
                filter=orm.Q(**applies_count_filter),
                distinct=True
            ),
            'manual_applies_count': orm.Count(
                'applies',
                filter=orm.Q(**manual_applies_count_filter),
                distinct=True
            ),
        }
        qs = qs.annotate(**annotations).order_by(
            '-autoapplies_count',
            '-applies_count',
            '-manual_applies_count'
        )
        return qs

    def get_data_for_csv_report(self, request):
        queryset = self.get_queryset(request)
        queryset = queryset.annotate(
            name=functions.Concat(
                'user__first_name',
                orm.Value(' '),
                'user__last_name'),
            email=orm.F('user__email')
        )
        return queryset


@admin.register(models.JobSeekerRegistrationReport,
                site=base_admin.base_admin_site)
class JobSeekerRegistrationReportsAdmin(
        mixins.ReportAdminMixin,
        mixins.AllowReadOnlyModelAdminMixin,
        admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'created_at',
    )
    list_display_links = None
    list_filter = (('created_at', range_filter.DateRangeFilter),)
    csv_filename = 'JobSeekerRegistrationReport'

    def name(self, job_seeker):
        return job_seeker.user.get_full_name()
    name.short_description = 'Name'

    def email(self, job_seeker):
        return job_seeker.user.email
    email.short_description = 'Email'

    def get_data_for_csv_report(self, request):
        queryset = super().get_data_for_csv_report(request)
        queryset = queryset.annotate(
            name=functions.Concat(
                'user__first_name',
                orm.Value(' '),
                'user__last_name'),
            email=orm.F('user__email')
        )
        return queryset
