import http

import pytest
import stripe
from dateutil import relativedelta
from django.utils import timezone

from leet import enums
from tests import api_requests

date_start = timezone.now()
date_end = date_start + relativedelta.relativedelta(months=+1)

RENEW_BILLING_CYCLE_EVENT = {
    'type': 'invoice.payment_succeeded',
    'data': {
        'object':
            {
                'billing_reason': 'subscription_cycle',
                'lines': {
                    'data': [
                        {
                            'period': {
                                'end': date_end.timestamp(),
                                'start': date_start.timestamp()
                            },
                            'subscription': '',
                        }
                    ]
                }
            }
    }
}

SUBSCRIPTION_CANCEL_EVENT = {
    'type': 'customer.subscription.deleted',
    'data': {
        'object': {
            'id': '',
            'plan': {
                'active': True,
                'metadata': {}
            }
        }
    }
}


class TestSubscriptionWebhooksAPI:
    @pytest.mark.usefixtures('subscription', 'job')
    def test_change_subscription_date_when_new_subscription_cycle_starts(
            self, anonym_client, company, enterprise_corporate_package_50,
            constract_event_mock):
        company.customer.balance.job_seekers_remain = 1
        company.customer.balance.save()
        sub_id = company.customer.subscriptions.filter(
            status=enums.SubscriptionStatusEnum.ACTIVE.name).first().stripe_id
        event = RENEW_BILLING_CYCLE_EVENT.copy()
        event['data']['object']['lines']['data'][0]['subscription'] = sub_id
        constract_event_mock.return_value = event
        resp = api_requests.subscription_webhook(
            anonym_client, data=event
        )
        assert resp.status_code == http.HTTPStatus.OK
        company.customer.balance.refresh_from_db()
        assert (company.customer.balance.job_seekers_total
                == enterprise_corporate_package_50.job_seekers_count)
        assert (company.customer.balance.job_seekers_remain
                == enterprise_corporate_package_50.job_seekers_count)
        assert (company.customer.balance.jobs_total
                == enterprise_corporate_package_50.jobs_count)
        assert (company.customer.balance.jobs_remain
                == enterprise_corporate_package_50.jobs_count - 1)
        active_subscription = company.customer.subscriptions.filter(
            status=enums.SubscriptionStatusEnum.ACTIVE.name).first()
        assert active_subscription.date_start == date_start
        assert active_subscription.date_end == date_end

    @pytest.mark.usefixtures('subscription')
    def test_drop_subscription_when_expired(
            self, anonym_client, company, constract_event_mock):
        sub_id = company.customer.subscriptions.filter(
            status=enums.SubscriptionStatusEnum.ACTIVE.name).first().stripe_id
        event = SUBSCRIPTION_CANCEL_EVENT.copy()
        event['data']['object']['id'] = sub_id
        constract_event_mock.return_value = event
        resp = api_requests.subscription_webhook(
            anonym_client, data=event
        )
        assert resp.status_code == http.HTTPStatus.OK
        company.customer.balance.refresh_from_db()
        assert not company.customer.balance.job_seekers_total
        assert not company.customer.balance.job_seekers_remain
        assert not company.customer.balance.jobs_total
        assert not company.customer.balance.jobs_remain
        assert not company.customer.subscriptions.filter(
            status=enums.SubscriptionStatusEnum.ACTIVE.name).exists()

    @pytest.mark.usefixtures(
        'scheduled_starter_subscription', 'job', 'job1', 'job2',
        'job3', 'job4')
    def test_purchase_scheduled_subscription_when_subscription_expired(
            self, anonym_client, company, starter_package, constract_event_mock):
        sub_id = company.customer.subscriptions.filter(
            status=enums.SubscriptionStatusEnum.ACTIVE.name).first().stripe_id
        event = SUBSCRIPTION_CANCEL_EVENT.copy()
        event['data']['object']['id'] = sub_id
        constract_event_mock.return_value = event
        resp = api_requests.subscription_webhook(
            anonym_client, data=event
        )
        assert resp.status_code == http.HTTPStatus.OK
        company.customer.balance.refresh_from_db()
        assert (company.customer.balance.job_seekers_total
                == starter_package.job_seekers_count)
        assert (company.customer.balance.job_seekers_remain
                == company.customer.balance.job_seekers_total)
        assert (company.customer.balance.jobs_total
                == starter_package.jobs_count)
        assert (company.customer.balance.jobs_remain == 0)
        assert company.customer.subscriptions.filter(
            status=enums.SubscriptionStatusEnum.ACTIVE.name).exists()
        assert (company.customer.subscriptions.filter(
            status=enums.SubscriptionStatusEnum.ACTIVE.name).first().plan
                == starter_package)
        assert (company.jobs.filter(status=enums.JobStatusEnum.ACTIVE.name).count()
                == 2)

    @pytest.mark.usefixtures(
        'scheduled_starter_subscription', 'job', 'job1', 'job2',
        'job3', 'job4')
    def test_jobs_are_moved_to_draft_if_purchase_of_next_subscription_failed(
            self, anonym_client, company, starter_package,
            mock_auto_renew_subscription_create, constract_event_mock):
        sub_id = company.customer.subscriptions.filter(
            status=enums.SubscriptionStatusEnum.ACTIVE.name).first().stripe_id
        event = SUBSCRIPTION_CANCEL_EVENT.copy()
        event['data']['object']['id'] = sub_id
        constract_event_mock.return_value = event
        mock_auto_renew_subscription_create.side_effect = \
            stripe.error.CardError(code='card_declined',
                                   message='Your card has insufficient funds.',
                                   param='')
        resp = api_requests.subscription_webhook(
            anonym_client, data=event
        )
        assert resp.status_code == http.HTTPStatus.OK
        company.customer.balance.refresh_from_db()
        assert company.customer.balance.job_seekers_total == 0
        assert company.customer.balance.job_seekers_remain == 0
        assert company.customer.balance.jobs_total == 0
        assert company.customer.balance.jobs_remain == 0
        assert not company.customer.subscriptions.filter(
            status=enums.SubscriptionStatusEnum.ACTIVE.name).exists()
        assert not company.jobs.filter(status=enums.JobStatusEnum.ACTIVE.name).count()

    def test_custom_plan_becomes_inactive_when_subscription_expired(
            self, anonym_client, company, custom_subscription,
            custom_subscription_plan, constract_event_mock):
        sub_id = company.customer.subscriptions.filter(
            status=enums.SubscriptionStatusEnum.ACTIVE.name).first().stripe_id
        event = SUBSCRIPTION_CANCEL_EVENT.copy()
        event['data']['object']['id'] = sub_id
        constract_event_mock.return_value = event
        resp = api_requests.subscription_webhook(
            anonym_client, data=event
        )
        assert resp.status_code == http.HTTPStatus.OK
        custom_subscription_plan.refresh_from_db()
        assert not custom_subscription_plan.is_active
