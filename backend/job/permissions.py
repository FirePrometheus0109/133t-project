from rest_framework import permissions as drf_permissions

from job import mixins
from leet import enums
from permission import permissions


class JobPermission(permissions.BaseModelPermissions,
                    permissions.BaseOwnerPermission):

    def has_permission(self, request, view):
        """Check permission for put and delete on object level."""
        if request.method == 'PUT' or request.method == 'DELETE':
            return True
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        """
        Object owner has all perms.
        """
        has_perm = super().has_object_permission(request, view, obj)
        if not has_perm:
            if request.method == 'GET':
                has_perm = request.user.has_perm('job.view_job')
            if request.method == 'PUT' or request.method == 'DELETE':
                has_perm = request.user.has_perms([
                    'job.change_job',
                    'job.delete_job'
                ])
        return has_perm


class BulkJobsDeletePermissions(drf_permissions.BasePermission):

    def has_permission(self, request, view):
        has_perm = request.user.has_perm('job.delete_job')
        if has_perm:
            # in case of job list deletion: check that all jobs
            # that should be deleted belong to user's company
            jobs = request.data.get('jobs', [])
            jobs_to_delete_count = len(jobs)
            company = request.user.company_user.company
            company_jobs_count = company.jobs.filter(id__in=jobs).count()
            return jobs_to_delete_count == company_jobs_count
        return has_perm


class RestoreJobPermission(drf_permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm('job.restore_job')


class DownloadJobCSVPermissions(drf_permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm('job.export_job_csv')


class CreateJobWithDelayedStatusPermission(
        mixins.JobAttributesPermissionMixin, drf_permissions.BasePermission):
    permission_name = 'job.create_delayed_job'
    field_to_check = 'status'

    def _check_field(self, request):
        return request.data.get('status') == enums.JobStatusEnum.DELAYED.name  # noqa


class CreateJobWithCoverLetterRequiredPermission(
        mixins.JobAttributesPermissionMixin, drf_permissions.BasePermission):
    permission_name = 'job.set_job_is_cover_letter_required'
    field_to_check = 'is_cover_letter_required'


class CreateJobWithClosingDatePermission(
        mixins.JobAttributesPermissionMixin, drf_permissions.BasePermission):
    permission_name = 'job.set_job_closing_date'
    field_to_check = 'closing_date'


class JobEnumPermission(drf_permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm('job.view_job_enum')


class ShareJobPermission(drf_permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm('job.share_job')
