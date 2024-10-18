from django.utils import timezone

from rest_framework import permissions

from subscription import constants
from subscription import utils


class SubscribePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        has_perm = request.user.has_perm(
            'subscription.purchase_subscription_plan'
        )
        return has_perm


class TrialSubscribePermission(SubscribePermission):
    message = constants.TRIAL_SUBSCRIPTION_IS_ALREADY_USED

    def has_permission(self, request, view):
        has_perm = super().has_permission(request, view)
        return (has_perm
                and request.user.company_user.company.is_trial_available)


class ViewActiveSubscriptionPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        has_perm = request.user.has_perm(
            'subscription.view_active_subscription'
        )
        return has_perm


class SubscriptionHasReportingPermission(permissions.BasePermission):
    """
    Allows access only if subscription supports reporting functionality.
    """

    message = constants.PLAN_HAS_NOT_REPORTING_ERROR

    def has_permission(self, request, view):
        if not hasattr(request.user, 'company_user'):
            return True
        active_subscription = utils.get_active_subscription(
            request.user.company_user.company)
        if active_subscription:
            return active_subscription.plan.is_reporting_enabled
        return True
