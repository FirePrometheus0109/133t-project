import mock
from dateutil import relativedelta
from django.conf import settings
from django.utils import timezone

from leet import enums
from subscription import tasks


class TestPlanDeletion:

    def test_plan_isnt_deleted_before_deletion_date_comes(
            self, company, subscription, deleted_corporate_package_50):
        months_count = settings.MONTHS_COUNT_BEFORE_PLAN_CHANGES_APPLY
        time_before_deletion_date = (
                timezone.now()
                + relativedelta.relativedelta(months=+months_count - 1)
        )
        with mock.patch('django.utils.timezone.now',
                        new=lambda: time_before_deletion_date):
            tasks.delete_subscription_plans.delay()
        deleted_corporate_package_50.refresh_from_db()
        assert deleted_corporate_package_50.is_active is True
        assert deleted_corporate_package_50.is_deleted is False
        assert (company.customer.subscriptions.first().plan
                == deleted_corporate_package_50)

    def test_plan_is_deleted_when_deletion_date_comes(
            self, company, subscription, mock_auto_renew_subscription_create,
            deleted_corporate_package_50, corporate_package_40, mailoutbox,
            active_company_user):
        mailoutbox.clear()
        months_count = settings.MONTHS_COUNT_BEFORE_PLAN_CHANGES_APPLY
        time_after_deletion_date = (
                timezone.now()
                + relativedelta.relativedelta(months=+months_count)
        )
        with mock.patch('django.utils.timezone.now',
                        new=lambda: time_after_deletion_date):
            tasks.delete_subscription_plans.delay()
        deleted_corporate_package_50.refresh_from_db()
        assert deleted_corporate_package_50.is_active is False
        assert deleted_corporate_package_50.is_deleted is True
        # check user subscription was handled
        assert len(company.customer.subscriptions.all()) == 1
        subscription = company.customer.subscriptions.first()
        assert (subscription.status
                == enums.SubscriptionStatusEnum.ACTIVE.name)
        assert subscription.plan == corporate_package_40
        assert len(mailoutbox) == 2

    def test_new_subscription_isnt_created_if_not_autorenew_subscription(
            self, subscription, deleted_corporate_package_50, company,
            mailoutbox):
        mailoutbox.clear()
        company.customer.auto_renew_subscription = False
        company.customer.save()
        months_count = settings.MONTHS_COUNT_BEFORE_PLAN_CHANGES_APPLY
        time_after_deletion_date = (
                timezone.now() + relativedelta.relativedelta(
            months=+months_count)
        )
        with mock.patch('django.utils.timezone.now',
                        new=lambda: time_after_deletion_date):
            tasks.delete_subscription_plans.delay()
        deleted_corporate_package_50.refresh_from_db()
        assert deleted_corporate_package_50.is_active is False
        assert deleted_corporate_package_50.is_deleted is True
        assert not len(company.customer.subscriptions.all())
        assert not len(mailoutbox)

    def test_create_subscription_to_scheduled_plan_if_current_deleted(
            self, scheduled_starter_subscription, starter_package,
            deleted_corporate_package_50, company, mailoutbox):
        mailoutbox.clear()
        company.customer.auto_renew_subscription = False
        company.customer.save()
        months_count = settings.MONTHS_COUNT_BEFORE_PLAN_CHANGES_APPLY
        time_after_deletion_date = (
                timezone.now()
                + relativedelta.relativedelta(months=+months_count)
        )
        with mock.patch('django.utils.timezone.now',
                        new=lambda: time_after_deletion_date):
            tasks.delete_subscription_plans.delay()
        deleted_corporate_package_50.refresh_from_db()
        assert deleted_corporate_package_50.is_active is False
        assert deleted_corporate_package_50.is_deleted is True
        assert len(company.customer.subscriptions.all()) == 1
        subscription = company.customer.subscriptions.first()
        assert (subscription.status
                == enums.SubscriptionStatusEnum.ACTIVE.name)
        assert subscription.plan == starter_package
        assert len(mailoutbox) == 1

    def test_create_subscription_to_custom_plan_if_current_deleted(
            self, subscription, custom_subscription_plan,
            deleted_corporate_package_50, company, mailoutbox):
        mailoutbox.clear()
        months_count = settings.MONTHS_COUNT_BEFORE_PLAN_CHANGES_APPLY
        time_after_deletion_date = (
                timezone.now()
                + relativedelta.relativedelta(months=+months_count)
        )
        with mock.patch('django.utils.timezone.now',
                        new=lambda: time_after_deletion_date):
            tasks.delete_subscription_plans.delay()
        deleted_corporate_package_50.refresh_from_db()
        assert deleted_corporate_package_50.is_active is False
        assert deleted_corporate_package_50.is_deleted is True
        assert len(company.customer.subscriptions.all()) == 1
        subscription = company.customer.subscriptions.first()
        assert (subscription.status
                == enums.SubscriptionStatusEnum.ACTIVE.name)
        assert subscription.plan == custom_subscription_plan
        assert len(mailoutbox) == 1

    def test_create_subscription_to_cheapest_plan_if_starter_deleted(
            self, starter_subscription, deleted_starter_package, company,
            basic_package_3, mailoutbox):
        mailoutbox.clear()
        months_count = settings.MONTHS_COUNT_BEFORE_PLAN_CHANGES_APPLY
        time_after_deletion_date = (
                timezone.now()
                + relativedelta.relativedelta(months=+months_count)
        )
        with mock.patch('django.utils.timezone.now',
                        new=lambda: time_after_deletion_date):
            tasks.delete_subscription_plans.delay()
        deleted_starter_package.refresh_from_db()
        assert deleted_starter_package.is_active is False
        assert deleted_starter_package.is_deleted is True
        assert len(company.customer.subscriptions.all()) == 1
        subscription = company.customer.subscriptions.first()
        assert (subscription.status
                == enums.SubscriptionStatusEnum.ACTIVE.name)
        assert subscription.plan == basic_package_3
        assert len(mailoutbox) == 1
