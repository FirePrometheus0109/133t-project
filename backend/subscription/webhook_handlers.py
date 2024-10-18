# pylint: disable=no-member
from django.db import transaction

from leet import enums
from leet import utils
from subscription import constants
from subscription import models
from subscription import services


def subscription_cancel(event):
    subscription_stripe_id = event['data']['object']['id']
    expired_subscription = models.Subscription.objects.filter(
        stripe_id=subscription_stripe_id,
        status=enums.SubscriptionStatusEnum.ACTIVE.name
    )
    if expired_subscription.exists():
        expired_subscription = expired_subscription.first()
        should_schedule_next_subscription = (
            _is_subscription_expired_because_of_price_changes(
                event, expired_subscription)
            and not expired_subscription.next_subscription
        )
        # add current plan as next subscription because of plan changes
        if should_schedule_next_subscription:
            service = services.SubscribeService(expired_subscription.owner)
            with transaction.atomic():
                service.schedule_subscription(expired_subscription,
                                              expired_subscription.plan)
        services.cancel_subscription(expired_subscription)


def payment_succeeded(event):
    invoice_object = event['data']['object']
    invoice_item = invoice_object['lines']['data'][0]
    if (invoice_object['billing_reason']
            == constants.SUBSCRIPTION_CYCLE_BILLING_REASON):
        subscription_stripe_id = invoice_item['subscription']
        timestamp_start = invoice_item['period']['start']
        timestamp_end = invoice_item['period']['end']
        date_start = utils.timestamp_to_utc_datetime(timestamp_start)
        date_end = utils.timestamp_to_utc_datetime(timestamp_end)
        services.renew_subscription_cycle(
            subscription_stripe_id, date_start, date_end
        )


def _is_subscription_expired_because_of_price_changes(
        event, expired_subscription):
    is_plan_active = event['data']['object']['plan']['active']
    is_updated_plan_exists = (
        event['data']['object']['plan']['metadata'].get('actual_id')
        == expired_subscription.plan.stripe_id
    )
    return not is_plan_active and is_updated_plan_exists
