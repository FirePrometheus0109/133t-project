from django.utils import timezone
from rest_framework import permissions

from leet import constants
from leet import enums
from leet import utils


class BaseOwnerPermission(permissions.BasePermission):
    """Default owner base permission for checking perms by owner."""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner.user


class BaseModelPermissions(permissions.DjangoModelPermissions):
    """
    Added permissions for method GET.
    """

    perms_map = {
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class HasSubscription(permissions.BasePermission):
    """
    Allows access only to users that have subscription.
    """
    message = constants.SUBSCRIPTION_REQUIRED_ERROR

    def has_permission(self, request, view):
        if hasattr(request.user, 'company_user'):
            company = request.user.company_user.company
            subscriptions = utils.get_from_nested_structure(
                company, ['customer', 'subscriptions'], func=getattr)
            active_subscription = None

            if subscriptions is not None:
                active_subscription = subscriptions.filter(
                    status=enums.SubscriptionStatusEnum.ACTIVE.name,  # noqa
                    date_end__gte=timezone.now()
                ).first()
            return bool(active_subscription)
        return True


# TODO(m.nizovtsova): it's going to be used for all create, update,
#  delete requests that are available for company
class CompanyProfileFilled(permissions.BasePermission):
    """
    Allows non-safe methods only for company with filled profile
    """
    message = constants.FILL_COMPANY_PROFILE_ERROR

    def has_permission(self, request, view):
        if (hasattr(request.user, 'company_user')
                and request.method not in permissions.SAFE_METHODS):
            company = request.user.company_user.company
            return company.is_profile_filled
        return True
