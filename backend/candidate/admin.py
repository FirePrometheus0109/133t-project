from django.contrib import admin

from candidate import models
from leet import admin as base_admin


@admin.register(models.Candidate, site=base_admin.base_admin_site)
class CandidateAdmin(base_admin.BaseModelAdmin):
    list_display = (
        'job_seeker',
        'job',
        'status',
        'previous_applied_date',
    )
    readonly_fields = (
        'previous_applied_date',
    )
    search_fields = (
        'job__title',
        'job_seeker__user__first_name',
        'job_seeker__user__last_name',
    )
    list_filter = (
        'status__name',
        'created_at',
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
