import datetime

import stripe
from dateutil import relativedelta
from django.conf import settings
from django.db import models as orm
from django.utils import timezone
from notifications import signals

from leet import emaillib
from leet import enums
from leet import utils
from notification_center import constants as notif_constants
from permission import constants as permission_constants
from subscription import constants
from subscription import models


def get_expiring_trial_subscriptions():
    subscription_end_days = (
        timezone.now().date()
        + datetime.timedelta(days=constants.FIRST_NOTIFICATION_DAYS_BEFORE),
        timezone.now().date()
        + datetime.timedelta(days=constants.SECOND_NOTIFICATION_DAYS_BEFORE)
    )
    subscription_end_hour = timezone.now().hour
    subscriptions = models.Subscription.objects.filter(
        orm.Q(is_trial=True)
        &
        orm.Q(date_end__date__in=subscription_end_days)
        &
        orm.Q(date_end__hour=subscription_end_hour)
    )
    return subscriptions


def get_payments_history(customer):
    payments_history = []
    has_more = True
    pagination_params = {}
    while has_more:
        stripe_invoices = stripe.Invoice.list(
            customer=customer.stripe_id, limit=100,
            **pagination_params
        )
        for invoice in stripe_invoices['data']:
            payments_history.append({
                'amount': utils.cents_to_dollars(
                    invoice['lines']['data'][0]['amount']),
                'plan': invoice['lines']['data'][0]['plan']['nickname'],
                'payment_date': utils.timestamp_to_utc_datetime(
                    invoice['finalized_at']
                ),
                'date_start': utils.timestamp_to_utc_datetime(
                    invoice['lines']['data'][0]['period']['start']
                ),
                'date_end': utils.timestamp_to_utc_datetime(
                    invoice['lines']['data'][0]['period']['end']
                ),
                'pdf_invoice_url': invoice['invoice_pdf']
            })
        has_more = stripe_invoices['has_more']
        if has_more:
            pagination_params = {
                'starting_after': stripe_invoices['data'][-1]['id']
            }
    return payments_history


def create_stripe_plan(plan_obj, stripe_product_id=None):
    # In case of only price changes there is no necessity
    # to create new stripe product. Do this only when create a new one.
    if stripe_product_id is None:
        stripe_product = stripe.Product.create(
            name=plan_obj.name,
            type='service'
        )
        stripe_product_id = stripe_product['id']
    stripe_plan = stripe.Plan.create(
        nickname=plan_obj.name,
        amount=int(plan_obj.price * constants.CENTS_IN_DOLLAR),
        product=stripe_product_id,
        interval='month',
        metadata={
            'is_custom': plan_obj.is_custom,
            'job_postings_number': plan_obj.jobs_count,
            'profile_views_number': plan_obj.job_seekers_count
        },
        currency=constants.USD_CURRENCY_ISO_CODE
    )
    return stripe_plan


def archive_stripe_plan(stripe_plan, updated_plan_id=None):
    # archive Stripe plan to make it unavailable for new customers.
    # If plan is archived because of changes, update its metadata.
    if updated_plan_id is not None:
        stripe_plan['metadata'].update({'actual_id': updated_plan_id})
    stripe_plan.active = False
    stripe_plan.save()


def cancel_plan_stripe_subscriptions_at_period_end(plan_stripe_id):
    # obtain all active Stripe subscriptions with auto renew
    active_subscriptions = []
    has_more = True
    pagination_params = {}
    while has_more:
        stripe_subscriptions = stripe.Subscription.list(
            status="active",
            plan=plan_stripe_id,
            limit=100,
            **pagination_params
        )
        active_subscriptions += stripe_subscriptions['data']
        has_more = stripe_subscriptions['has_more']
        if has_more:
            pagination_params = {
                'starting_after': stripe_subscriptions['data'][-1]['id']
            }
    for subscription in active_subscriptions:
        subscription.cancel_at_period_end = True
        subscription.save()


def get_plan_change_or_delete_apply_date():
    months_count = settings.MONTHS_COUNT_BEFORE_PLAN_CHANGES_APPLY
    return timezone.now() + relativedelta.relativedelta(months=+months_count)


def get_cheaper_plan(plan, company):
    """
    Return next cheaper plan or company custom plan if exist.
    :param plan: Plan object
    :param company: Company object
    :return: Plan object
    """
    custom_company_plan = models.Plan.objects.filter(
        company=company, deletion_date__isnull=True).first()
    if custom_company_plan:
        return custom_company_plan
    cheaper_plan = models.Plan.objects.filter(
        price__lt=plan.price,
        deletion_date__isnull=True,
        company__isnull=True
    ).order_by('-price').first()
    if not cheaper_plan:
        # if the cheapest plan was deleted than return
        # the cheapest plan from available ones
        cheaper_plan = models.Plan.objects.filter(
            deletion_date__isnull=True, company__isnull=True
        ).order_by('price').first()
    return cheaper_plan


def notify_users_about_plan_deletion(plan):
    contexts = []
    url = settings.COMPANY_DASHBOARD_URL.format(
        http=settings.HTTP_SCHEME,
        domain_name=settings.DOMAIN_NAME,
    )
    subscriptions = models.Subscription.objects.filter(
        plan=plan,
        status=enums.SubscriptionStatusEnum.ACTIVE.name)  # noqa
    for subscription in subscriptions:
        company_users = get_company_subscription_managers(
            subscription.customer.company
        )
        next_plan = (subscription.next_subscription.plan
                     if subscription.next_subscription
                     else get_cheaper_plan(subscription.plan,
                                           subscription.customer.company))
        for cu in company_users:
            contexts.append({
                'domain_name': settings.DOMAIN_NAME,
                'user': cu.user,
                'deletion_date': plan.deletion_date,
                'plan': plan.name,
                'url': url,
                'next_plan': next_plan.name

            })
            send_web_notification_about_plan_deletion(
                cu.user, plan, next_plan.name)
    emaillib.send_emails(
        constants.SUBSCRIPTION_PLAN_DELETE_TEMPLATE_NAME, contexts
    )


def send_web_notification_about_plan_deletion(
        user, current_plan, next_plan_name):
    date_formatted = current_plan.deletion_date.strftime(
        settings.DEFAULT_SERVER_DATE_FORMAT
    )
    description = (
        notif_constants.NOTIFICATION_DESCRIPTION_PACKAGE_WILL_DELETED.format(
            date_formatted, current_plan.name, next_plan_name
        )
    )
    verb = notif_constants.NOTIFICATION_VERB_PACKAGE_WILL_DELETED
    signals.notify.send(
        current_plan,
        recipient=user,
        verb=verb,
        description=description,
        data={
            'short': {
                'plan': {
                    'id': current_plan.id,
                    'title': current_plan.name
                }
            },
            'full': {
                'plan': {
                    'description': description
                }
            }
        }
    )


def notify_users_about_price_changes(plan):
    contexts = []
    subscriptions = models.Subscription.objects.filter(
        plan=plan,
        status=enums.SubscriptionStatusEnum.ACTIVE.name)  # noqa
    for subscription in subscriptions:
        company_users = get_company_subscription_managers(
            subscription.customer.company
        )
        for cu in company_users:
            contexts.append({
                'domain_name': settings.DOMAIN_NAME,
                'user': cu.user,
                'new_price': plan.new_price,
                'price_apply_date': plan.price_apply_date,

            })
            send_web_notification_about_price_changes(cu.user, plan)
    emaillib.send_emails(
        constants.SUBSCRIPTION_PRICE_CHANGE_TEMPLATE_NAME, contexts
    )


def send_web_notification_about_price_changes(
        user, plan):
    date_formatted = plan.price_apply_date.strftime(
        settings.DEFAULT_SERVER_DATE_FORMAT
    )
    description = (
        notif_constants.NOTIFICATION_DESCRIPTION_PRICE_WAS_CHANGED.format(
            price_apply_date=date_formatted, new_price=plan.new_price
        )
    )
    verb = notif_constants.NOTIFICATION_VERB_PACKAGE_PRICE_CHANGED
    signals.notify.send(
        plan,
        recipient=user,
        verb=verb,
        description=description,
        data={
            'short': {
                'plan': {
                    'id': plan.id,
                    'title': plan.name
                }
            },
            'full': {
                'plan': {
                    'description': description
                }
            }
        }
    )


def get_company_subscription_managers(company):
    """
    Returns company users that can manage subscriptions.
    """
    return company.company_users.filter(
        user__groups__name=permission_constants.MANAGE_SUBSCRIPTION_PLAN_GROUP
    )


def get_active_subscription(company):
    subscriptions = utils.get_from_nested_structure(company, ['customer', 'subscriptions'], func=getattr)
    active_subscription = None

    if subscriptions is not None:
        active_subscription = subscriptions.filter(
            status=enums.SubscriptionStatusEnum.ACTIVE.name,  # noqa
            date_end__gte=timezone.now()
        ).first()
        return active_subscription