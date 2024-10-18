from rest_framework import permissions
from permission import utils


class JobSeekerSetPasswordWithoutOldPasswordPermission(
        permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if utils.is_job_seeker(user) and not user.job_seeker.is_password_set:
            return True
        return False
