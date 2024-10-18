#  pylint: disable=no-member
import itertools

import stripe
from django.conf import settings
from django.utils import timezone
from notifications import signals

from leet import enums
from leet import utils as base_utils
from leet.emaillib import send_emails
from leet.taskapp.celery import app
from notification_center import constants as notif_constants
from subscription import constants as s_constants
from subscription import models
from subscription import services
from subscription import utils


@app.task(name='send-trial-expiration-notifications')
def send_trial_expiration_notifications():
    """
    Notify user 5 days before trial subscription will end and 1 day before.
    """
    subscriptions = utils.get_expiring_trial_subscriptions()
    contexts = []
    for s in subscriptions:
        date_suffix = 'nd' if s.date_end.day in (2, 12, 22) else 'th'
        url = settings.COMPANY_DASHBOARD_URL.format(
            http=settings.HTTP_SCHEME,
            domain_name=settings.DOMAIN_NAME,
        )
        subscription_managers = utils.get_company_subscription_managers(
            s.customer.company
        )
        date_end = s.date_end.strftime(
            settings.DATE_FORMAT_FOR_TRIAL_EXPIRES_EMAIL_TEMPLATE.format(
                suffix=date_suffix
            )
        )
        for cu in subscription_managers:
            _notify_about_trial_end(s, cu.user, date_end)
            context = {
                'domain_name': settings.DOMAIN_NAME,
                'user': cu.user,
                'date_end': date_end,
                'url': url
            }
            contexts.append(context)
    send_emails(
        s_constants.TRIAL_SUBSCRIPTION_NOTIFICATION_TEMPLATE_NAME, contexts
    )


@app.task(name='delete-subscription-plans')
def delete_subscription_plans():
    """
    Delete subscription plans when deletion date is coming
    """
    plans_for_deletion = models.Plan.admin_objects.filter(
        is_deleted=False, deletion_date__lte=timezone.now()
    )
    user_emails_contexts = []
    url = settings.COMPANY_DASHBOARD_URL.format(
        http=settings.HTTP_SCHEME,
        domain_name=settings.DOMAIN_NAME,
    )
    for plan in plans_for_deletion:
        active_subscriptions = (
            models.Subscription.objects.filter(
                plan=plan,
                status=enums.SubscriptionStatusEnum.ACTIVE.name
            )
        )
        try:
            for subscription in active_subscriptions:
                service = services.SubscribeService(subscription.owner)
                next_cheaper_plan = utils.get_cheaper_plan(
                    subscription.plan, subscription.customer.company
                )
                if all((not subscription.next_subscription,
                        next_cheaper_plan,
                        subscription.customer.auto_renew_subscription)):
                    service.schedule_subscription(
                        subscription, next_cheaper_plan
                    )
                # TODO (m.nizovtsova): force unsubscribe from current
                # plan anyway, need to be discussed with BA
                services.delete_stripe_subscription(subscription.stripe_id)
                new_subscription = services.cancel_subscription(
                    subscription
                )
                if new_subscription:
                    company_users = utils.get_company_subscription_managers(
                        new_subscription.customer.company
                    )
                    for cu in company_users:
                        user_emails_contexts.append({
                            'user': cu.user,
                            'deleted_plan': plan.name,
                            'new_plan': new_subscription.plan.name,
                            'url': url,
                        })
                        _notify_about_plan_deletion(
                            plan, new_subscription.plan.name, cu.user)
        except stripe.errors.StripeError:
            # something went wrong with Stripe,
            # try one more time while next task run
            continue
        else:
            plans_for_deletion.update(is_deleted=True, is_active=False)
    send_emails(
        s_constants.SUBSCRIPTION_PLAN_CHANGE_TEMPLATE_NAME,
        user_emails_contexts
    )


@app.task(name='update-plan-prices')
def update_plan_prices():
    changed_plans = models.Plan.admin_objects.filter(
        is_active=True, is_deleted=False, new_price__isnull=False,
        price_apply_date__lte=timezone.now()
    )
    for plan in changed_plans:
        try:
            old_plan_stripe_obj = stripe.Plan.retrieve(plan.stripe_id)
            stripe_product_id = old_plan_stripe_obj['product']

            plan.price = plan.new_price
            plan.new_price = None
            plan.price_apply_date = None

            stripe_plan_with_new_price = utils.create_stripe_plan(
                plan, stripe_product_id
            )
            plan.stripe_id = stripe_plan_with_new_price['id']

            utils.cancel_plan_stripe_subscriptions_at_period_end(
                old_plan_stripe_obj['id']
            )
            utils.archive_stripe_plan(old_plan_stripe_obj,
                                      stripe_plan_with_new_price['id'])
            plan.save()
        except stripe.errors.StripeError:
            # something went wrong with Stripe,
            # try one more time while next task run
            continue


@app.task(name='sync-customer-invoices')
def sync_customer_invoices():
    latest_invoice = (models.Invoice.objects.all()
                      .order_by('-datetime_of_payment').first())
    datetime_filter = {}
    if latest_invoice:
        last_date_timestamp = int(
            latest_invoice.datetime_of_payment.timestamp()
        )
        datetime_filter = {'created': {'gte': last_date_timestamp}}
    invoices = get_stripe_invoices(datetime_filter)
    grouped_invoices = itertools.groupby(invoices, key=lambda x: x['customer'])
    for customer_id, invoices in grouped_invoices:
        customer = (
            models.Customer.objects.filter(stripe_id=customer_id).first()
        )
        if customer:
            # don't use bulk create to avoid of integrity error
            # because of uniqueness violations
            for invoice in invoices:
                models.Invoice.objects.get_or_create(
                    customer=customer,
                    stripe_id=invoice['id'],
                    amount=invoice['amount'],
                    datetime_of_payment=invoice['date'],
                    description=invoice['description']
                )


def get_stripe_invoices(dt_filter=None):
    invoices = []
    has_more = True
    pagination_params = {}
    datetime_filter = {}
    if dt_filter:
        datetime_filter = dt_filter
    while has_more:
        stripe_invoices = stripe.Invoice.list(
            limit=100,
            **pagination_params,
            **datetime_filter
        )
        for invoice in stripe_invoices['data']:
            invoices.append({
                'id': invoice['id'],
                'customer': invoice['customer'],
                'amount': base_utils.cents_to_dollars(
                    invoice['lines']['data'][0]['amount']),
                'date': base_utils.timestamp_to_utc_datetime(
                    invoice['finalized_at']),
                'description': invoice['lines']['data'][0]['description']
            })
        has_more = stripe_invoices['has_more']
        if has_more:
            pagination_params = {
                'starting_after': stripe_invoices['data'][-1]['id']
            }
    return invoices


def _notify_about_trial_end(subscription, user, date_end):
    description = notif_constants.NOTIFICATION_DESCRIPTION_END_OF_TRIAL.format(
        date_end
    )
    verb = notif_constants.NOTIFICATION_VERB_END_OF_TRIAL
    signals.notify.send(
        subscription,
        recipient=user,
        verb=verb,
        description=description,
        data={
            'full': {
                'subscription': {
                    'description': description
                }
            }
        }
    )


def _notify_about_plan_deletion(deleted_plan, current_plan_name, user):
    description = (
        notif_constants.NOTIFICATION_DESCRIPTION_PACKAGE_WAS_DELETED.format(
            deleted_plan.name, current_plan_name
        )
    )
    verb = notif_constants.NOTIFICATION_VERB_PACKAGE_WAS_DELETED
    signals.notify.send(
        deleted_plan,
        recipient=user,
        verb=verb,
        description=description,
        data={
            'full': {
                'plan': {
                    'description': description
                }
            }
        }
    )
