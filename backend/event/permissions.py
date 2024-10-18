from rest_framework import permissions as drf_permissions

from event import models
from permission import permissions
from permission import utils as perm_utils


class EventPermission(permissions.BaseModelPermissions):

    def has_permission(self, request, view):
        if perm_utils.is_job_seeker(request.user):
            return False
        if (request.method == 'PUT' or
                request.method == 'PATCH' or
                request.method == 'DELETE'):
            return True
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        """Owner has all permission for his event."""
        has_perm = request.user == obj.owner
        if not has_perm:
            perms = self.get_required_permissions(request.method, models.Event)
            return request.user.has_perms(perms)
        return has_perm


class AnotherEventPermission(drf_permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm('event.check_another_event')
