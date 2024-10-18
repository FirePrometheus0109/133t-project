import datetime
import http

import mock
import pytest
import stripe
from django.conf import settings
from django.utils import timezone

from leet import enums
from leet import constants as leet_constants
from subscription import constants
from subscription import tasks
from tests import api_requests
from tests import utils
from tests import validators
from tests.api.subscription import expected


class TestTrialSubscriptionAPI:

    @pytest.mark.usefixtures('mock_subscription_trial_create')
    def test_trial_subscribe_success(
            self, company_user_client_without_subscription,
            trial_subscription_plans):
        plan = utils.get_random_database_object(trial_subscription_plans)
        resp = api_requests.subscribe_to_trial_plan(
            company_user_client_without_subscription, data={'plan': plan.id})
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json() == expected.EXPECTED_TRIAL_SUBSCRIPTION

    def test_trial_subscribe_to_deleted_plan_fails(
            self, company_user_client_without_subscription,
            deleted_corporate_package_50):
        resp = api_requests.subscribe_to_trial_plan(
            company_user_client_without_subscription,
            data={'plan': deleted_corporate_package_50.id}
        )
        emsg = constants.PLAN_CANT_BE_SELECTED
        validators.validate_error_message(resp, emsg, 'plan')

    @pytest.mark.usefixtures('mock_subscription_trial_create')
    def test_trial_subscribe_fails_if_company_was_already_subscribed_to_trial(
            self, company_user_client_without_subscription,
            trial_subscription_plans):
        plan = utils.get_random_database_object(trial_subscription_plans)
        resp = api_requests.subscribe_to_trial_plan(
            company_user_client_without_subscription, data={'plan': plan.id})
        assert resp.status_code == http.HTTPStatus.CREATED
        resp = api_requests.subscribe_to_trial_plan(
            company_user_client_without_subscription, data={'plan': plan.id})
        emsg = constants.TRIAL_SUBSCRIPTION_IS_ALREADY_USED
        http_code = http.HTTPStatus.FORBIDDEN
        validators.validate_error_message(resp, emsg, error_code=http_code)

    @pytest.mark.usefixtures('mock_subscription_trial_create')
    def test_job_seeker_has_no_access_to_subscriptions(
            self, job_seeker_client, trial_subscription_plans):
        plan = utils.get_random_database_object(trial_subscription_plans)
        resp = api_requests.subscribe_to_trial_plan(
            job_seeker_client, data={'plan': plan.id})
        assert resp.status_code == http.HTTPStatus.FORBIDDEN

    def test_send_email_to_company_users_with_manage_subscription_perm_when_trial_expires(
            self, company_user_client,
            active_company_user, mailoutbox):
        mailoutbox.clear()
        trial_period_length = settings.TRIAL_PERIOD_LENGTH
        five_days_before_subscription_ends_date = (
                timezone.now() + datetime.timedelta(
            days=trial_period_length - 5)
        )
        with mock.patch('django.utils.timezone.now',
                        new=lambda: five_days_before_subscription_ends_date):
            tasks.send_trial_expiration_notifications.delay()
        assert len(mailoutbox) == 2


class TestSubscriptionAPI:

    def test_subscribe_during_trial_subscription_success(
            self, company_user_client,
            enterprise_corporate_package_50,
            mock_auto_renew_subscription_create, company,
            billing_information_auto_renew):
        resp = api_requests.subscribe(
            company_user_client, data={
                'plan': enterprise_corporate_package_50.id,
            }
        )
        assert resp.status_code == http.HTTPStatus.CREATED
        actual_subscription = resp.json()
        assert actual_subscription == expected.EXPECTED_AUTORENEW_SUBSCRIPTION
        mock_auto_renew_subscription_create.assert_called_once_with(
            customer=company.customer.stripe_id,
            plan=enterprise_corporate_package_50.stripe_id,
            cancel_at_period_end=False
        )
        assert (actual_subscription['balance']['job_seekers_total']
                == enterprise_corporate_package_50.job_seekers_count)
        assert (actual_subscription['balance']['job_seekers_remain']
                == enterprise_corporate_package_50.job_seekers_count)
        assert (actual_subscription['balance']['jobs_total']
                == enterprise_corporate_package_50.jobs_count)
        assert (actual_subscription['balance']['jobs_remain']
                == enterprise_corporate_package_50.jobs_count)

    @pytest.mark.parametrize(('plan_fixture',), (
            ('enterprise_corporate_package_75',),
            ('enterprise_corporate_package_50',)
    ))
    def test_upgrade_or_renew_subscription(
            self, company_user_client, subscription,
            mock_not_auto_renew_subscription_create,
            company, request, plan_fixture, enterprise_corporate_package_50,
            billing_information_not_auto_renew):
        plan = request.getfixturevalue(plan_fixture)
        company.customer.balance.job_seekers_remain = 10
        company.customer.balance.save()
        current_job_seekers_total_balance = company.customer.balance.job_seekers_total
        current_job_seekers_remain_balance = company.customer.balance.job_seekers_remain
        current_jobs_total_balance = company.customer.balance.jobs_total
        current_jobs_remain_balance = company.customer.balance.jobs_remain
        resp = api_requests.subscribe(
            company_user_client, data={
                'plan': plan.id
            }
        )
        assert resp.status_code == http.HTTPStatus.CREATED
        actual_subscription = resp.json()
        assert actual_subscription == expected.EXPECTED_NOT_AUTORENEW_SUBSCRIPTION
        mock_not_auto_renew_subscription_create.assert_called_once_with(
            customer=company.customer.stripe_id,
            plan=plan.stripe_id,
            cancel_at_period_end=True
        )
        assert (actual_subscription['balance']['job_seekers_total']
                == current_job_seekers_total_balance + plan.job_seekers_count)
        assert (actual_subscription['balance']['job_seekers_remain']
                == current_job_seekers_remain_balance + plan.job_seekers_count)
        assert (actual_subscription['balance']['jobs_total']
                == current_jobs_total_balance + plan.jobs_count)
        assert (actual_subscription['balance']['jobs_remain']
                == current_jobs_remain_balance + plan.jobs_count)

    def test_downgrade_subscription(
            self, company_user_client, subscription, corporate_package_40,
            mock_not_auto_renew_subscription_create, company,
            billing_information_not_auto_renew):
        current_job_seekers_total_balance = company.customer.balance.job_seekers_total
        current_job_seekers_remain_balance = company.customer.balance.job_seekers_remain
        current_jobs_total_balance = company.customer.balance.jobs_total
        current_jobs_remain_balance = company.customer.balance.jobs_remain
        resp = api_requests.subscribe(
            company_user_client, data={
                'plan': corporate_package_40.id
            }
        )
        assert resp.status_code == http.HTTPStatus.CREATED
        actual_subscription = resp.json()
        assert actual_subscription == expected.EXPECTED_DOWNGRADED_SUBSCRIPTION
        mock_not_auto_renew_subscription_create.assert_not_called()
        assert (actual_subscription['balance']['job_seekers_total']
                == current_job_seekers_total_balance)
        assert (actual_subscription['balance']['job_seekers_remain']
                == current_job_seekers_remain_balance)
        assert (actual_subscription['balance']['jobs_total']
                == current_jobs_total_balance)
        assert (actual_subscription['balance']['jobs_remain']
                == current_jobs_remain_balance)

    def test_purchase_subscription_fails_if_payment_doesnt_succeed(
            self, company_user_client, subscription,
            mock_auto_renew_subscription_create,
            company, enterprise_corporate_package_75,
            enterprise_corporate_package_50):
        mock_auto_renew_subscription_create.side_effect = \
            stripe.error.CardError(code='card_declined',
                                   message='Your card has insufficient funds.',
                                   param='')
        resp = api_requests.subscribe(
            company_user_client, data={
                'plan': enterprise_corporate_package_75.id,
            }
        )
        emsg = constants.FAILED_TO_PROCESS_PAYMENT_ERROR
        http_code = http.HTTPStatus.UNPROCESSABLE_ENTITY
        validators.validate_error_message(resp, emsg, error_code=http_code)

    def test_purchase_subscription_fails_for_deleted_plan(
            self, company_user_client, subscription,
            company, deleted_corporate_package_50):
        resp = api_requests.subscribe(
            company_user_client, data={
                'plan': deleted_corporate_package_50.id,
            }
        )
        emsg = constants.PLAN_CANT_BE_SELECTED
        validators.validate_error_message(resp, emsg, 'plan')

    def test_purchase_subscription_fails_if_no_payment_data_provided(
            self, company_user_client,
            enterprise_corporate_package_50,
            mock_auto_renew_subscription_create, company,):
        resp = api_requests.subscribe(
            company_user_client, data={
                'plan': enterprise_corporate_package_50.id,
            }
        )
        emsg = constants.BILLING_INFORMATION_REQUIRED_ERROR
        validators.validate_error_message(resp, emsg)

    def test_get_active_subscription_success(
            self, company_user_client, subscription):
        resp = api_requests.get_active_subscription(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json() == expected.EXPECTED_AUTORENEW_SUBSCRIPTION

    def test_unsubscribe_from_plan_success(
            self, company_user_client, enterprise_corporate_package_50,
            company, subscription):
        resp = api_requests.unsubscribe(
            company_user_client,
            subscription['id'])
        assert resp.status_code == http.HTTPStatus.OK
        company_active_subscription = company.customer.subscriptions.filter(
            status=enums.SubscriptionStatusEnum.ACTIVE.name
        ).first()
        assert not company_active_subscription.is_auto_renew
        assert not company.customer.auto_renew_subscription

    def test_cancel_next_subscription_success(
            self, company_user_client, company, subscription,
            scheduled_starter_subscription):
        resp = api_requests.unsubscribe(
            company_user_client,
            scheduled_starter_subscription['next_subscription']['id'])
        assert resp.status_code == http.HTTPStatus.OK
        company_active_subscription = company.customer.subscriptions.filter(
            status=enums.SubscriptionStatusEnum.ACTIVE.name
        ).first()
        assert company_active_subscription.is_auto_renew
        assert not company_active_subscription.next_subscription

    def test_create_job_without_subscription(
            self, company_user_client_without_subscription, job_base_data):
        resp = api_requests.create_job(
            company_user_client_without_subscription,
            job_base_data)
        emsg = leet_constants.SUBSCRIPTION_REQUIRED_ERROR
        http_code = http.HTTPStatus.FORBIDDEN
        validators.validate_error_message(resp, emsg, error_code=http_code)
