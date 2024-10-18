# pylint: disable=no-member
from django.contrib.admin import SimpleListFilter

from leet import enums


class UserFilter(SimpleListFilter):
    title = 'type'
    parameter_name = 'type'

    def lookups(self, request, model_admin):
        return (
            (enums.UserTypeEnum.ADMIN.name, '133T users'),
            (enums.UserTypeEnum.COMPANY_USER.name, 'Company users'),
            (enums.UserTypeEnum.JOB_SEEKER.name, 'Job seekers'),
        )

    def queryset(self, request, queryset):
        if self.value() == enums.UserTypeEnum.ADMIN.name:
            queryset = queryset.filter(company_user=None, job_seeker=None)
        elif self.value() == enums.UserTypeEnum.COMPANY_USER.name:
            queryset = queryset.filter(company_user__isnull=False)
        elif self.value() == enums.UserTypeEnum.JOB_SEEKER.name:
            queryset = queryset.filter(job_seeker__isnull=False)
        return queryset
