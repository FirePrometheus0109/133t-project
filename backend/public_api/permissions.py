from rest_framework import permissions
from public_api import constants

from job_seeker import constants as js_constants


class JobSeekerPublicProfilePermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if not obj.is_shared:
            self.message = constants.PROFILE_IS_NOT_AVAILABLE_ERROR  # noqa
            return False
        if not obj.is_public or obj.is_deleted:
            self.message = js_constants.PROFILE_IS_HIDDEN_ERROR  # noqa
            return False
        return True
