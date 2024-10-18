# pylint: disable=no-member
from django.conf import settings
from rest_framework import exceptions

from leet import enums
from subscription import constants


def validate_plan(plan, company):
    """
    Raises ValidationError if company user tries to subscribe
    to custom plan that doesn't belong his company.
    """
    if plan.company and plan.company != company:
        raise exceptions.ValidationError(
            constants.CANT_SUBSCRIBE_TO_NOT_YOUR_COMPANY_PLAN
        )


def validate_plan_isnt_for_deletion(plan):
    """
    Raises ValidationError if company user tries to subscribe
    to plan that is going to be deleted
    """
    if plan.deletion_date:
        raise exceptions.ValidationError(
            constants.PLAN_CANT_BE_SELECTED
        )


def validate_next_subscription_hasnt_chosen(company):
    if hasattr(company, 'customer'):
        customer = company.customer
        active_subscription = customer.subscriptions.filter(
            status=enums.SubscriptionStatusEnum.ACTIVE.name,
            next_subscription__isnull=False
        )
        if active_subscription.exists():
            next_subscription = active_subscription.first().next_subscription
            next_plan_name = next_subscription.plan.name
            next_start_date = next_subscription.date_start
            next_end_date = next_subscription.date_end
            raise exceptions.ValidationError(
                constants.YOU_ALREADY_PURCHASED_SUBSCRIPTION.format(
                    plan=next_plan_name,
                    date_start=next_start_date.strftime(
                        settings.DEFAULT_SERVER_DATE_FORMAT),
                    date_end=next_end_date.strftime(
                        settings.DEFAULT_SERVER_DATE_FORMAT)
                )
            )


def validate_billing_information(plan, customer):
    if not plan.price == 0 and not customer.is_billing_info_provided:
        raise exceptions.ValidationError(
            constants.BILLING_INFORMATION_REQUIRED_ERROR
        )
