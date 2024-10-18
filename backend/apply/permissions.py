from rest_framework import permissions as drf_permissions

from apply import constants
from permission import permissions


class AutoApplyJobListPermission(drf_permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm('apply.view_autoapply_jobs')


class AutoApplyJobDetailPermission(drf_permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm('apply.view_autoapply_job_detail')


class StartAutoApplyPermission(permissions.BaseOwnerPermission):
    message = constants.PROFILE_ISNT_PUBLIC_ERROR

    def has_permission(self, request, view):
        has_perm = request.user.has_perm('apply.start_autoapply')
        return has_perm and request.user.job_seeker.is_public


class StopAutoApplyPermission(permissions.BaseOwnerPermission):

    def has_permission(self, request, view):
        return request.user.has_perm('apply.stop_autoapply')


class RestartAutoApplyPermission(permissions.BaseOwnerPermission):

    def has_permission(self, request, view):
        return request.user.has_perm('apply.restart_autoapply')


class AutoApplyToJobPermission(permissions.BaseOwnerPermission):
    message = constants.PROFILE_ISNT_PUBLIC_ERROR

    def has_permission(self, request, view):
        has_perm = request.user.has_perm('apply.autoapply_to_job')
        return has_perm and request.user.job_seeker.is_public


class AppliedJobsPermission(drf_permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm('apply.view_applied_jobs')


class ApplyPermission(drf_permissions.BasePermission):
    message = constants.PROFILE_ISNT_PUBLIC_ERROR

    def has_permission(self, request, view):
        has_perm = request.user.has_perm('apply.add_apply')
        return has_perm and request.user.job_seeker.is_public


class ReApplyPermission(drf_permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm('apply.do_reapply')


class AutoApplyStatsPermission(drf_permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm('apply.view_autoapply_stats')
