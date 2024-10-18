import http

import pytest

from tests import api_requests
from tests import clients
from tests import constants


@pytest.fixture
def anonym_client(db):
    """Use this fixture if you need to send request as anonym user"""
    return clients.JWTClient()


@pytest.fixture
def job_seeker_client(job_seeker):
    """Use this fixture if you need to send request as job seeker"""
    creds = {
        'email': job_seeker.user.email,
        'password': constants.DEFAULT_PASSWORD
    }
    client = clients.JWTClient()
    client.login(**creds)
    return client


@pytest.fixture
def job_seeker_2_client(job_seeker_2):
    """Use this fixture if you need to send request as other job seeker"""
    creds = {
        'email': job_seeker_2.user.email,
        'password': constants.DEFAULT_PASSWORD
    }
    client = clients.JWTClient()
    client.login(**creds)
    return client


@pytest.fixture
def company_user_client_without_subscription(company_user):
    """Use this fixture if you need to send request as company user."""
    creds = {
        'email': company_user.user.email,
        'password': constants.DEFAULT_PASSWORD
    }
    client = clients.JWTClient()
    client.login(**creds)
    return client


@pytest.fixture
def company_user_client(
        company_user_client_without_subscription, trial_subscription):
    """Use this fixture if you need to send request as company user.
    Company has Subscription"""
    return company_user_client_without_subscription


@pytest.fixture
def company_2_user_client_without_subscription(company_2_user):
    """Use this fixture if you need to send request as other company user.
    Company user works at second test company"""
    creds = {
        'email': company_2_user.user.email,
        'password': constants.DEFAULT_PASSWORD
    }
    client = clients.JWTClient()
    client.login(**creds)
    return client


@pytest.fixture
def company_2_user_client(
        company_2_user_client_without_subscription,
        trial_subscription_company_2):
    """Use this fixture if you need to send request as other company user.
    Company user works at second test company. Company has Subscription"""
    return company_2_user_client_without_subscription


@pytest.fixture
def company_user_2_creds(active_company_user):
    return {
        'email': active_company_user['user']['email'],
        'password': constants.DEFAULT_PASSWORD
    }


@pytest.fixture
def company_user_2_client(company_user_2_creds):
    """Use this fixture if you need to send request as new company user
    This user have same company as `company_user`
    """
    client = clients.JWTClient()
    client.login(**company_user_2_creds)
    return client


@pytest.fixture
def company_draft_client(
        company_draft_user, enterprise_corporate_package_75,
        customer_create_mock, mock_subscription_trial_create):
    creds = {
        'email': company_draft_user.user.email,
        'password': constants.DEFAULT_PASSWORD
    }
    client = clients.JWTClient()
    client.login(**creds)

    customer_create_mock.return_value = {'id': 'cust_draft'}
    data = {'plan': enterprise_corporate_package_75.id}
    resp = api_requests.subscribe_to_trial_plan(client, data)
    assert resp.status_code == http.HTTPStatus.CREATED
    return client
