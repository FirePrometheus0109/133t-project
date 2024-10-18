#  pylint: disable=too-many-arguments,comparison-with-callable,no-member
import datetime

import stripe
from dateutil import relativedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import DatabaseError
from django.db import models as orm
from django.db import transaction
from rest_framework import exceptions as api_exceptions

from leet import enums
from leet import exceptions
from leet import utils as base_utils
from permission import constants as perm_constants
from permission import models as perm_models
from permission import utils
from subscription import constants
from subscription import models

User = get_user_model()


class SubscribeService:
    def __init__(self, company_user):
        self.company_user = company_user
        self.company = self.company_user.company
        self.customer = self._get_or_create_customer()

    def get_subscription_lock(self):
        try:
            scheduled_subscription = self.get_scheduled_subscription()
            if scheduled_subscription:
                draft = scheduled_subscription
            else:
                draft = (
                    models.Subscription.objects
                    .create(customer=self.customer,
                            owner=self.company_user)
                )
            subscription_lock = (
                models.Subscription.objects
                .select_for_update(nowait=True)
                .get(id=draft.id)
            )
            return subscription_lock
        except DatabaseError:
            raise exceptions.PurchaseSubscriptionError(
                constants.PURCHASE_SUBSCRIPTION_FAILED_BECAUSE_OF_DATABASE_LOCK
            )

    def get_scheduled_subscription(self):
        subscription = self.customer.subscriptions.filter(
            status=enums.SubscriptionStatusEnum.SCHEDULED.name)
        return subscription.first() if subscription.exists() else None

    def trial_subscribe(self, plan):
        trial_period_length = settings.TRIAL_PERIOD_LENGTH
        try:
            draft_subscription = self.get_subscription_lock()
            stripe_subscription = self.create_stripe_subscription(
                customer=self.customer.stripe_id,
                plan=plan.stripe_id,
                cancel_at_period_end=True,
                trial_period_days=trial_period_length
            )
        except stripe.error.StripeError:
            raise exceptions.PurchaseSubscriptionError(
                constants.FAILED_TO_PURCHASE_TRIAL_SUBSCRIPTION_ERROR
            )
        else:
            self.apply_plan_restrictions(plan)
            self.set_balance(plan.job_seekers_count,
                             plan.jobs_count)
            self.disable_trial_for_company()
            subscription = self.activate_subscription(
                draft_subscription, stripe_subscription, plan
            )
            return subscription

    @staticmethod
    def activate_subscription(subscription, stripe_subscription, plan):
        subscription.stripe_id = stripe_subscription['id']
        subscription.date_start = base_utils.timestamp_to_utc_datetime(
            stripe_subscription['current_period_start']
        )
        subscription.date_end = base_utils.timestamp_to_utc_datetime(
            stripe_subscription['current_period_end']
        )
        is_trial = stripe_subscription['status'] == 'trialing'
        subscription.is_auto_renew = not stripe_subscription[
            'cancel_at_period_end']
        subscription.is_trial = is_trial
        subscription.plan = plan
        subscription.status = enums.SubscriptionStatusEnum.ACTIVE.name
        subscription.save()
        return subscription

    @staticmethod
    def create_stripe_subscription(**kwargs):
        return stripe.Subscription.create(**kwargs)

    def disable_trial_for_company(self):
        self.company.is_trial_available = False
        self.company.save()

    def set_balance(self, job_seekers_cnt, jobs_cnt,
                    reset=True, is_checkout_plan_process=False):
        with transaction.atomic():
            customer_balance = (models.Balance.objects
                                .select_for_update()
                                .get(customer=self.customer))
            if reset:
                self.reset_balance(
                    customer_balance, job_seekers_cnt,
                    jobs_cnt, is_checkout_plan_process)
            else:
                self.upgrade_balance(
                    customer_balance, job_seekers_cnt, jobs_cnt)
            customer_balance.save()

    @staticmethod
    def reset_balance(
            balance, job_seekers_cnt, jobs_cnt, is_checkout_plan_process):
        balance.job_seekers_total = job_seekers_cnt
        balance.job_seekers_remain = job_seekers_cnt

        balance.jobs_total = jobs_cnt
        active_or_delayed_jobs = (
            balance.customer.company.jobs.filter(status__in=[
                enums.JobStatusEnum.ACTIVE.name,
                enums.JobStatusEnum.DELAYED.name,
            ])
        )
        jobs_count = active_or_delayed_jobs.count()
        if jobs_count > balance.jobs_total and not is_checkout_plan_process:
            jobs_out_of_limit_ids = (
                active_or_delayed_jobs
                .values_list('id', flat=True)
                .order_by('created_at')[balance.jobs_total:]
            )
            balance.customer.company.jobs.filter(
                id__in=jobs_out_of_limit_ids
            ).update(status=enums.JobStatusEnum.DRAFT.name)
        jobs_remain = balance.jobs_total - jobs_count
        balance.jobs_remain = jobs_remain if jobs_remain >= 0 else 0

    @staticmethod
    def upgrade_balance(balance, job_seekers_cnt, jobs_cnt):
        balance.job_seekers_total = (orm.F('job_seekers_total')
                                     + job_seekers_cnt)
        balance.job_seekers_remain = (orm.F('job_seekers_remain')
                                      + job_seekers_cnt)
        balance.jobs_total = orm.F('jobs_total') + jobs_cnt
        balance.jobs_remain = orm.F('jobs_remain') + jobs_cnt

    def subscribe(self, plan, is_trial=False):
        subscribe_method = self._purchase_subscription
        current_subscription_stripe_id = None
        if is_trial and self.company.is_trial_available:
            subscribe_method = self.trial_subscribe
        subscription = self.customer.subscriptions.filter(
            status=enums.SubscriptionStatusEnum.ACTIVE.name)
        if subscription.exists():
            current_subscription = subscription.first()
            current_subscription_stripe_id = current_subscription.stripe_id
            if current_subscription.is_trial:
                subscribe_method = self._purchase_subscription
            else:
                current_plan = current_subscription.plan
                if plan.price >= current_plan.price:
                    subscribe_method = self._upgrade_subscription
                else:
                    subscribe_method = self.downgrade_subscription

        with transaction.atomic():
            subscription = subscribe_method(plan=plan)
        if (current_subscription_stripe_id
                and subscribe_method != self.downgrade_subscription):
            self._delete_subscription(current_subscription_stripe_id)
        return subscription

    def apply_plan_restrictions(self, plan):
        self.apply_permissions_limitations(plan)
        if plan.price:
            self._enable_company_users()
        else:
            self._apply_jobs_restrictions()
            self._disable_company_users()

    def apply_permissions_limitations(self, plan):
        users = User.objects.filter(
            company_user__in=self.company.company_users.all())
        if plan.price:
            self._remove_permissions_limitations(users)
        else:
            self._set_permissions_limitations(
                users, perm_constants.STARTER_SUBSCRIPTION_RESTRICTED_PERMS)

    @staticmethod
    def _set_permissions_limitations(users, permissions_list):
        utils.delete_permissions_for_user_list(
            users, permissions_list,
            enums.CustomPermissionReasonEnum.SUBSCRIPTION_LIMIT.name)

    @staticmethod
    def _remove_permissions_limitations(users):
        perm_models.UserCustomPermission.objects.filter(
            user__in=users,
            action=enums.ActionEnum.DELETE.value,
            reason=enums.CustomPermissionReasonEnum.SUBSCRIPTION_LIMIT.name
        ).delete()

    def _apply_jobs_restrictions(self):
        company_jobs = self.company.jobs
        (company_jobs.filter(status=enums.JobStatusEnum.DELAYED.name)
                     .update(status=enums.JobStatusEnum.DRAFT.name,
                             publish_date=None))
        (company_jobs.filter(is_cover_letter_required=True)
                     .update(is_cover_letter_required=False))
        (company_jobs.update(closing_date=None))

    def _disable_company_users(self):
        first_subscription_manager_id = (
            self.company.company_users.filter(
                user__groups__name=perm_constants.MANAGE_SUBSCRIPTION_PLAN_GROUP  # noqa
            ).order_by('created_at').values_list('id', flat=True)[0])
        (self.company.company_users.filter(
            ~orm.Q(id=first_subscription_manager_id)
        ).update(is_disabled_by_subscription=True))

    def _enable_company_users(self):
        (self.company.company_users
         .filter(is_disabled_by_subscription=True)
         .update(is_disabled_by_subscription=False))

    def _delete_subscription(self, subscription_stripe_id):
        delete_stripe_subscription(subscription_stripe_id)
        models.Subscription.objects.filter(
            customer=self.customer,
            stripe_id=subscription_stripe_id,
            status=enums.SubscriptionStatusEnum.ACTIVE.name
        ).delete()

    def unsubscribe(self, subscription, set_to_customer=True):
        if subscription.status == enums.SubscriptionStatusEnum.ACTIVE.name:
            if subscription.is_auto_renew:
                stripe_subscription = stripe.Subscription.retrieve(
                    id=subscription.stripe_id)
                stripe_subscription.cancel_at_period_end = True
                stripe_subscription.save()
                subscription.is_auto_renew = False
                subscription.save()
            # If `set_to_customer` is False it shouldn't be changed in customer
            # instance, this attribute can be False only in case of downgrade
            # of subscription to unsubscribe only from current subscription.
            if set_to_customer:
                subscription.customer.auto_renew_subscription = False
                subscription.customer.save()
        elif (subscription.status
              == enums.SubscriptionStatusEnum.SCHEDULED.name):
            subscription.delete()
            self.update_subscription_auto_renew(
                self.customer.auto_renew_subscription)

    def update_subscription_auto_renew(self, auto_renew):
        subscription = self.customer.subscriptions.filter(
            status=enums.SubscriptionStatusEnum.ACTIVE.name,
            is_trial=False
        ).first()
        if subscription and not subscription.next_subscription:
            stripe_subscription = stripe.Subscription.retrieve(
                id=subscription.stripe_id)
            if not auto_renew or stripe_subscription['plan']['active']:
                # Because of plan archivation (in case of price changes)
                # it's needed to make sure that user doesn't
                # try to set cancel_at_period_end=False for subscription
                # to archived plan. All such subscriptions
                # should expire at most 1 month later after price changes.
                stripe_subscription.cancel_at_period_end = not auto_renew
                stripe_subscription.save()
            subscription.is_auto_renew = auto_renew
            subscription.save()

    def _upgrade_subscription(self, plan):
        return self._purchase_subscription(reset_balance=False, plan=plan)

    def downgrade_subscription(self, plan):
        current_subscription = (
            models.Subscription.objects
            .select_for_update(nowait=True)
            .get(customer=self.customer,
                 status=enums.SubscriptionStatusEnum.ACTIVE.name)
        )
        self.unsubscribe(current_subscription, set_to_customer=False)
        self.schedule_subscription(current_subscription, plan)
        return current_subscription

    def schedule_subscription(
            self, current_subscription, plan):
        scheduled_subscription = self.get_subscription_lock()
        is_auto_renew = self.customer.auto_renew_subscription
        scheduled_subscription.plan = plan
        scheduled_subscription.is_auto_renew = is_auto_renew
        scheduled_subscription.date_start = (
            current_subscription.date_end + datetime.timedelta(seconds=1)
        )
        scheduled_subscription.date_end = (
            scheduled_subscription.date_start
            + relativedelta.relativedelta(months=+1))
        scheduled_subscription.status = (
            enums.SubscriptionStatusEnum.SCHEDULED.name
        )
        scheduled_subscription.save()
        current_subscription.next_subscription = scheduled_subscription
        current_subscription.save()
        return scheduled_subscription

    def _purchase_subscription(self, plan, reset_balance=True):
        is_auto_renew = self.customer.auto_renew_subscription
        try:
            draft_subscription = self.get_subscription_lock()
            stripe_subscription = self.create_stripe_subscription(
                customer=self.customer.stripe_id,
                plan=plan.stripe_id,
                cancel_at_period_end=not is_auto_renew
            )
        except stripe.error.StripeError:
            raise exceptions.PurchaseSubscriptionError(
                constants.FAILED_TO_PROCESS_PAYMENT_ERROR)
        else:
            self.customer.subscriptions.filter(
                status=enums.SubscriptionStatusEnum.ACTIVE.name).delete()
            self.apply_plan_restrictions(plan)
            self.set_balance(plan.job_seekers_count,
                             plan.jobs_count, reset_balance)
            subscription = self.activate_subscription(
                draft_subscription, stripe_subscription, plan
            )
            return subscription

    def _get_or_create_customer(self):
        company = self.company_user.company
        if not hasattr(self.company_user.company, 'customer'):
            stripe_customer = stripe.Customer.create()
            models.Customer.objects.create(
                stripe_id=stripe_customer['id'],
                company=company,
                balance=models.Balance.objects.create(),
            )
        return company.customer


class BillingInformationService:
    def __init__(self, company_user):
        self.company_user = company_user
        self.customer = company_user.company.customer

    def set_billing_information(self, token, email, auto_renew_subscription):
        self.customer = (models.Customer.objects
                         .select_for_update().get(id=self.customer.id))
        stripe_customer = stripe.Customer.retrieve(self.customer.stripe_id)

        try:
            payment_source = stripe_customer.sources.create(source=token)
        except stripe.error.StripeError:
            # TODO (i.bogretsov) add error message instead of default
            raise api_exceptions.APIException()
        stripe_customer.default_source = payment_source['id']
        stripe_customer.email = email
        stripe_customer.save()
        self.customer.auto_renew_subscription = auto_renew_subscription
        self.customer.is_billing_info_provided = True
        SubscribeService(self.company_user).update_subscription_auto_renew(
            auto_renew_subscription)
        self.customer.save()


def renew_subscription_cycle(subscription_stripe_id,
                             date_start, date_end):
    with transaction.atomic():
        subscription = (models.Subscription.objects
                        .select_for_update()
                        .get(stripe_id=subscription_stripe_id))
        subscription.date_start = date_start
        subscription.date_end = date_end
        subscription.save()
        SubscribeService(subscription.owner).set_balance(
            subscription.plan.job_seekers_count,
            subscription.plan.jobs_count
        )


def cancel_subscription(subscription):
    """
    Delete inactive subscription from db. Subscribe company to the next
    scheduled subscription if exist.
    :param subscription:
    :return: new subscription object or None
    """
    next_subscription = subscription.next_subscription
    expired_plan = subscription.plan
    customer = subscription.customer
    if expired_plan.is_custom:
        # Custom subscription plans available for customer
        # only while customer is paying it
        expired_plan.is_active = False
        expired_plan.save()
    subscription.delete()
    SubscribeService(customer).set_balance(
        0, 0, reset=True,
        is_checkout_plan_process=True if next_subscription else False)
    if next_subscription:
        company_user = next_subscription.owner
        try:
            subscription = SubscribeService(company_user).subscribe(
                next_subscription.plan
            )
        except exceptions.PurchaseSubscriptionError:
            SubscribeService(customer).set_balance(0, 0)
        else:
            return subscription
    return None


def delete_stripe_subscription(subscription_stripe_id):
    subscription = stripe.Subscription.retrieve(
        id=subscription_stripe_id)
    subscription.delete()
