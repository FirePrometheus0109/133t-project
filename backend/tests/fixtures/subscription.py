import datetime
import http

import mock
import pytest
from dateutil import relativedelta
from django.conf import settings
from django.utils import timezone

from subscription import models, constants
from tests import api_requests


@pytest.fixture(autouse=True)
def customer_create_mock(mocker, db):
    create_mock = mock.MagicMock(
        return_value={'id': 'cust'}
    )
    mocker.patch('stripe.Customer.create', create_mock)
    return create_mock


@pytest.fixture(autouse=True)
def customer_retrieve_mock(mocker):
    retrieve_mock = mock.MagicMock()
    retrieve_mock.return_value.sources.create.return_value = {
        'id': 'payment_source_id'
    }
    retrieve_mock.save = mock.MagicMock()
    mocker.patch('stripe.Customer.retrieve', retrieve_mock)
    return retrieve_mock


@pytest.fixture(autouse=True)
def subscription_retrieve_mock(mocker):
    subscription_mock = mock.MagicMock()
    mocker.patch('stripe.Subscription.retrieve', subscription_mock)
    return subscription_mock


@pytest.fixture(autouse=True)
def plan_retrieve_mock(mocker):
    retrieve_mock = mock.MagicMock({
        'id': 'plan_id',
        'product': 'product_id',
        'metadata': {}
    })
    retrieve_mock.return_value.save = mock.MagicMock()
    mocker.patch('stripe.Plan.retrieve', retrieve_mock)
    return retrieve_mock


@pytest.fixture(autouse=True)
def create_stripe_plan_mock(mocker):
    stripe_id = 'plan_{}'.format(timezone.now().timestamp())
    plan_mock = mock.MagicMock(return_value={'id': stripe_id})
    mocker.patch('stripe.Product.create',
                 mock.Mock(return_value={'id': 'prod_id'}))
    mocker.patch('stripe.Plan.create', plan_mock)
    return plan_mock


@pytest.fixture(autouse=True)
def stripe_subscription_list_mock(mocker):
    list_mock = mock.MagicMock()
    mocker.patch('stripe.Subscription.list', list_mock)
    return list_mock


@pytest.fixture(autouse=True)
def constract_event_mock(mocker):
    constract_event_mock = mock.MagicMock()
    mocker.patch('stripe.Webhook.construct_event', constract_event_mock)
    return constract_event_mock


@pytest.fixture
def mock_subscription_trial_create(mocker):
    subscription_stripe_id = 'sub_{}'.format(
        timezone.now().timestamp()
    )
    subscription_create_mock = mocker.patch('stripe.Subscription.create')
    subscription_create_mock.return_value = {
        'id': subscription_stripe_id,
        'status': 'trialing',
        'cancel_at_period_end': True,
        'current_period_start': timezone.now().timestamp(),
        'current_period_end': (
                timezone.now()
                + datetime.timedelta(days=settings.TRIAL_PERIOD_LENGTH)
        ).timestamp(),
    }


@pytest.fixture
def mock_auto_renew_subscription_create(mocker):
    subscription_stripe_id = 'sub_{}'.format(
        timezone.now().timestamp()
    )
    subscription_create_mock = mocker.patch('stripe.Subscription.create')
    subscription_create_mock.return_value = {
        'id': subscription_stripe_id,
        'status': 'active',
        'cancel_at_period_end': False,
        'current_period_start': timezone.now().timestamp(),
        'current_period_end': (
                timezone.now() + relativedelta.relativedelta(months=+1)
        ).timestamp(),
    }
    return subscription_create_mock


@pytest.fixture
def mock_not_auto_renew_subscription_create(mocker):
    subscription_stripe_id = 'sub_{}'.format(
        timezone.now().timestamp()
    )
    subscription_create_mock = mocker.patch('stripe.Subscription.create')
    subscription_create_mock.return_value = {
        'id': subscription_stripe_id,
        'status': 'active',
        'cancel_at_period_end': True,
        'current_period_start': timezone.now().timestamp(),
        'current_period_end': (
                timezone.now() + relativedelta.relativedelta(months=+1)
        ).timestamp(),
    }
    return subscription_create_mock


@pytest.fixture
def subscription_plans(db):
    for plan in constants.DEFAULT_PLANS:
        stripe_plan_id = 'plan_{}'.format(models.Plan.objects.count())
        models.Plan.objects.create(
            stripe_id=stripe_plan_id,
            name=plan['name'],
            job_seekers_count=plan['metadata']['profile_views_number'],
            jobs_count=plan['metadata']['job_postings_number'],
            price=plan['price'],
            is_reporting_enabled=True,
            users_number=10,
        )
    return models.Plan.objects.filter(is_custom=False)


@pytest.fixture
def trial_subscription_plans(subscription_plans):
    return subscription_plans.filter(price__gt=0)


@pytest.fixture
def enterprise_corporate_package_50(subscription_plans):
    return subscription_plans.get(
        name=constants.ENTERPRISE_CORPORATE_PACKAGE_50['name']
    )


@pytest.fixture
def enterprise_corporate_package_75(subscription_plans):
    return subscription_plans.get(
        name=constants.ENTERPRISE_CORPORATE_PACKAGE_75['name']
    )


@pytest.fixture
def corporate_package_40(subscription_plans):
    return subscription_plans.get(
        name=constants.CORPORATE_PACKAGE_40['name']
    )


@pytest.fixture
def deleted_corporate_package_50(subscription_plans):
    plan = subscription_plans.get(
        name=constants.ENTERPRISE_CORPORATE_PACKAGE_50['name']
    )
    months_count = settings.MONTHS_COUNT_BEFORE_PLAN_CHANGES_APPLY
    plan.deletion_date = (
            timezone.now()
            + relativedelta.relativedelta(months=+months_count)
    )
    plan.save()
    return plan


@pytest.fixture
def corporate_package_50_new_price(subscription_plans):
    plan = subscription_plans.get(
        name=constants.ENTERPRISE_CORPORATE_PACKAGE_50['name']
    )
    months_count = settings.MONTHS_COUNT_BEFORE_PLAN_CHANGES_APPLY
    plan.new_price = 9999
    plan.price_apply_date = (
            timezone.now()
            + relativedelta.relativedelta(months=+months_count)
    )
    plan.save()
    return plan


@pytest.fixture
def basic_package_3(subscription_plans):
    return subscription_plans.get(
        name=constants.BASIC_PACKAGE_3['name']
    )


@pytest.fixture
def starter_package(subscription_plans):
    return subscription_plans.get(
        name=constants.STARTER_PACKAGE['name']
    )


@pytest.fixture
def deleted_starter_package(starter_package):
    months_count = settings.MONTHS_COUNT_BEFORE_PLAN_CHANGES_APPLY
    starter_package.deletion_date = (
            timezone.now()
            + relativedelta.relativedelta(months=+months_count)
    )
    starter_package.save()
    return starter_package


@pytest.fixture
def custom_subscription_plan(company):
    custom_plan = models.Plan.objects.create(
        stripe_id='custom_plan',
        name='Custom plan',
        job_seekers_count=1000,
        jobs_count=1000,
        price=0,
        is_custom=True,
        company=company
    )
    return custom_plan


@pytest.fixture
def deleted_custom_subscription_plan(custom_subscription_plan):
    months_count = settings.MONTHS_COUNT_BEFORE_PLAN_CHANGES_APPLY
    custom_subscription_plan.deletion_date = (
            timezone.now()
            + relativedelta.relativedelta(months=+months_count)
    )
    custom_subscription_plan.save()
    return custom_subscription_plan


@pytest.fixture
def trial_subscription(
        company_user_client_without_subscription,
        enterprise_corporate_package_75,
        mock_subscription_trial_create, customer_create_mock):
    customer_create_mock.return_value = {'id': 'cust_1'}
    resp = api_requests.subscribe_to_trial_plan(
        company_user_client_without_subscription,
        data={'plan': enterprise_corporate_package_75.id}
    )
    assert resp.status_code == http.HTTPStatus.CREATED


@pytest.fixture
def billing_information_auto_renew(
        trial_subscription, company_user_client_without_subscription):
    resp = api_requests.create_payment_source(
        company_user_client_without_subscription, data={
            'token': 'token',
            'email': 'email@mail.com',
            'auto_renew_subscription': True
        }
    )
    assert resp.status_code == http.HTTPStatus.CREATED


@pytest.fixture
def billing_information_not_auto_renew(
        trial_subscription, company_user_client_without_subscription):
    resp = api_requests.create_payment_source(
        company_user_client_without_subscription, data={
            'token': 'token',
            'email': 'email@mail.com',
            'auto_renew_subscription': False
        }
    )
    assert resp.status_code == http.HTTPStatus.CREATED


@pytest.fixture
def subscription(
        trial_subscription, company_user_client_without_subscription,
        mock_auto_renew_subscription_create, enterprise_corporate_package_50,
        billing_information_auto_renew
):
    """Company subscription to Enterprise Corporate Package-50"""
    resp = api_requests.subscribe(
        company_user_client_without_subscription, data={
            'plan': enterprise_corporate_package_50.id
        }
    )
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()


@pytest.fixture
def custom_subscription(
        trial_subscription, company_user_client_without_subscription,
        mock_auto_renew_subscription_create, custom_subscription_plan,
        billing_information_auto_renew
):
    """Company subscription to Custom plan"""
    resp = api_requests.subscribe(
        company_user_client_without_subscription, data={
            'plan': custom_subscription_plan.id
        }
    )
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()


@pytest.fixture
def subscription_with_75_jobs(
        trial_subscription, company_user_client_without_subscription,
        mock_auto_renew_subscription_create, enterprise_corporate_package_75,
        billing_information_auto_renew
):
    """Company subscription to Enterprise Corporate Package-75"""
    resp = api_requests.subscribe(
        company_user_client_without_subscription, data={
            'plan': enterprise_corporate_package_75.id
        }
    )
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()


@pytest.fixture
def trial_subscription_company_2(
        company_2_user_client_without_subscription,
        enterprise_corporate_package_75,
        mock_subscription_trial_create, customer_create_mock):
    customer_create_mock.return_value = {'id': 'cust_2'}
    resp = api_requests.subscribe_to_trial_plan(
        company_2_user_client_without_subscription,
        data={'plan': enterprise_corporate_package_75.id}
    )
    assert resp.status_code == http.HTTPStatus.CREATED


@pytest.fixture
def scheduled_starter_subscription(
        company_user_client, starter_package, subscription
):
    resp = api_requests.subscribe(
        company_user_client, data={
            'plan': starter_package.id
        }
    )
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()


@pytest.fixture
def subscription_basic_package_3(
        company_user_client,
        mock_auto_renew_subscription_create, basic_package_3,
        billing_information_auto_renew
):
    resp = api_requests.subscribe(
        company_user_client, data={
            'plan': basic_package_3.id
        }
    )
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()


@pytest.fixture
def starter_subscription(company_user_client, starter_package,
                         mock_auto_renew_subscription_create,
                         billing_information_auto_renew):
    resp = api_requests.subscribe(
        company_user_client, data={
            'plan': starter_package.id
        }
    )
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()
