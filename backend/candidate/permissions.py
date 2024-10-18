from rest_framework import permissions

from permission import utils


class JobCandidatePermission(permissions.BasePermission):
    """Only company user can watch candidates for company jobs"""

    def has_permission(self, request, view):
        has_perm = request.user.has_perm('job.view_job_candidates')
        if has_perm and view.kwargs:  # fix swagger
            company = request.user.company_user.company
            jobs_ids = company.jobs.values_list('id', flat=True)
            return view.kwargs.get('pk') in jobs_ids
        return has_perm


class CandidateAnswersPermission(permissions.DjangoModelPermissions):
    """
    Permissions for view job's questions' answers.
    A Job seeker can watch only his answers.
    A company user can watch answers only for jobs of his company.
    """

    def has_permission(self, request, view):

        has_perm = super().has_permission(request, view)

        if request.method == 'GET':
            if has_perm and view.kwargs:  # fix swagger
                user = request.user
                if utils.is_company_user(user):
                    job_id = view.kwargs.get('job_id')
                    jobs = (user.company_user
                                .company
                                .jobs
                                .values_list('id', flat=True))
                    return job_id in jobs
                if utils.is_job_seeker(user):
                    js_id = view.kwargs.get('job_seeker_id')
                    return user.job_seeker.id == js_id
            return has_perm

        return has_perm


class CandidateAssignPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        has_perm = request.user.has_perm('candidate.add_candidate')
        if has_perm:
            jobs = request.data.get('jobs', [])
            count = len(jobs)
            company = request.user.company_user.company
            company_jobs_count = company.jobs.filter(id__in=jobs).count()
            return count == company_jobs_count
        return has_perm


class CandidateRatingPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm('candidate.can_rate_candidate')


class CandidateRestorePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm('candidate.restore_candidate')


class WorkflowStepsCompanyStatsPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm('candidate.view_workflowstep_stats')


class CandidatesActivityPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm('candidate.view_candidate_activity')


class CandidateQuickListPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.has_perm('candidate.view_quick_list')
        return False


class ExportCandidateToCSVPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm('candidate.export_candidate_csv')


class CandidateEnumPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm('candidate.view_candidate_enum')
