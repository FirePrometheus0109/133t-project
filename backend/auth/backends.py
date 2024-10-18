# pylint: disable=inconsistent-return-statements,protected-access
from django.contrib import auth
from django.contrib.auth import backends

from auth import constants
from auth import services
from permission import utils

User = auth.get_user_model()


class EmailBackend(backends.ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User._default_manager.get(
                email__iexact=kwargs.get('email', None)
            )
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            User().set_password(password)
        else:
            is_password_correct = user.check_password(password)
            can_authenticate = self.user_can_authenticate(user)
            if is_password_correct:
                if not can_authenticate:
                    if utils.is_job_seeker(user):
                        service = services.UserAccountService(user)
                        service.send_restore_account_email(
                            constants.RESTORE_ACCOUNT_TEMPLATE_NAME)
                return user

    def get_all_permissions(self, user_obj, obj=None):
        """
        This is default 'get_all_permissions' method of model backend.
        Just added support for user custom permissions.
        """
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()
        if not hasattr(user_obj, '_perm_cache'):
            perms = {
                *self.get_user_permissions(user_obj),
                *self.get_group_permissions(user_obj),
            }
            custom_perms = utils.get_user_custom_permissions(user_obj)
            perms = utils.union_user_perms_with_custom_perms(
                perms, custom_perms)
            user_obj._perm_cache = perms
        return user_obj._perm_cache
