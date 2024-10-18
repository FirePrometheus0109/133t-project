from rest_framework import permissions


class JobAttributesPermissionMixin:
    field_to_check = None
    permission_name = None

    def has_permission(self, request, view):
        has_perm = request.user.has_perm(self.permission_name)
        if (request.method not in permissions.SAFE_METHODS
                and not has_perm and self._check_field(request)):
            return False
        return True

    def _check_field(self, request):
        return request.data.get(self.field_to_check)
