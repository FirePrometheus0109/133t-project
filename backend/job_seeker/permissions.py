from rest_framework import permissions as drf_permissions

from job_seeker import constants
from leet import services
from permission import permissions
from permission import utils


def can_company_view_profile(company, job_seeker):
    is_profile_hidden = not job_seeker.is_public or job_seeker.is_deleted
    return (not is_profile_hidden
            or services.is_user_candidate_for_company(job_seeker, company))


class JobSeekerProfilePermission(permissions.BaseModelPermissions):

    def has_permission(self, request, view):
        has_perm = super().has_permission(request, view)
        user = request.user
        if utils.is_company_user(user):
            return has_perm
        return has_perm and view.kwargs.get('pk')

    def has_object_permission(self, request, view, obj):

        if utils.is_company_user(request.user):
            self.message = constants.PROFILE_IS_HIDDEN_ERROR  # noqa
            company = request.user.company_user.company
            return can_company_view_profile(company, obj)

        return request.user == obj.user


class PhotoPermission(drf_permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm('job_seeker.upload_photo')

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class JobExperiencePermission(permissions.BaseModelPermissions,
                              permissions.BaseOwnerPermission):
    """Permissions for JobExperienceViewSet"""

    def has_permission(self, request, view):
        """
        All authorized users can view job seeker's experience
        Job seeker can create job experience only for himself.
        """

        has_perm = super().has_permission(request, view)

        if has_perm and view.kwargs:  # swagger fix
            js_id = view.kwargs.get('job_seeker_id')
            if utils.is_job_seeker(request.user):
                return has_perm and js_id == request.user.job_seeker.id

        return has_perm

    def has_object_permission(self, request, view, obj):
        """Delete and Update job experience can only owner"""
        has_perm = super().has_object_permission(request, view, obj)
        return request.method in drf_permissions.SAFE_METHODS or has_perm


class CertificationPermission(JobExperiencePermission):
    """
    Permissions for CertificationViewSet.
    Logic is the same as IsUserJobExperience"""


class EducationPermission(JobExperiencePermission):
    """
    Permissions for EducationViewSet.
    Logic is the same as IsUserJobExperience"""


class CoverLetterPermission(JobExperiencePermission):
    """
    Permissions for CoverLetterViewSet.
    Logic is the same as IsUserJobExperience
    """


class DocumentPermission(JobExperiencePermission):
    """
    Permissions for DocumentViewSet.
    Logic is the same as JobExperiencePermission.
    """


class SavedJobsPermission(drf_permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.has_perm('job_seeker.add_savedjob')

        if request.method == 'GET':
            return request.user.has_perm('job_seeker.view_savedjob')

        return False


class JobSeekerProfilePurchasePermission(drf_permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm('job_seeker.purchase_js_profile')


class PurchasedJobSeekersListPermission(drf_permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm('job_seeker.view_purchased_job_seekers')


class JobSeekerViewerListPermission(drf_permissions.BasePermission):

    def has_permission(self, request, view):
        has_perm = request.user.has_perm('job_seeker.view_viewjobseeker')
        if has_perm and view.kwargs:
            job_seeker_pk = view.kwargs.get('pk')
            return job_seeker_pk == request.user.job_seeker.id
        return has_perm


class SavedJobSeekerPermission(drf_permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm('job_seeker.add_savedjobseeker')
