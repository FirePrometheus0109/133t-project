import http

import pytest

from company import constants as company_constants
from tests import api_requests
from tests import validators


def test_unpurchased_job_seeker_profile_details(
        company_user_client, job_seeker):
    resp = api_requests.get_job_seeker_details(
        company_user_client,
        job_seeker.id)
    assert resp.status_code == http.HTTPStatus.OK
    data = resp.json()
    assert 'phone' not in data
    assert 'email' not in data['user']
    assert 'address' not in data
    assert not data['is_purchased']


def test_contact_info_is_hidden_even_if_job_seeker_has_apply(
        company_user_client, job_seeker, apply):
    resp = api_requests.get_job_seeker_details(
        company_user_client,
        job_seeker.id)
    assert resp.status_code == http.HTTPStatus.OK
    data = resp.json()
    assert 'phone' not in data
    assert 'email' not in data['user']
    assert 'address' not in data
    assert data['is_applied']
    assert not data['is_purchased']

def test_purchased_job_seeker_fields(
        company_user_client, purchased_job_seeker, document):
    resp = api_requests.get_job_seeker_details(
        company_user_client,
        purchased_job_seeker.id)
    assert resp.status_code == http.HTTPStatus.OK
    data = resp.json()
    assert 'phone' in data
    assert 'email' in data['user']
    assert 'address' in data
    assert data['documents']
    assert data['is_purchased']



class TestPurchaseJobSeeker:

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED
        ),
        (
            'company_user_client',
            http.HTTPStatus.OK
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.FORBIDDEN
        )
    ))
    def test_purchase_job_seeker_permissions(
            self, request, job_seeker, client, status):
        client = request.getfixturevalue(client)
        resp = api_requests.purchase_job_seeker(client, job_seeker.id)
        assert resp.status_code == status

    def test_purchase_job_seeker_success(
            self, company_user_client, job_seeker):
        resp = api_requests.purchase_job_seeker(
            company_user_client,
            job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        data = resp.json()
        assert 'phone' in data
        assert 'email' in data['user']
        assert 'address' in data
        assert data['is_purchased']

    def test_purchase_job_seeker_success_js_has_apply_for_job_other_company(
            self, company_user_client, job_seeker, apply_for_company_2_job):
        resp = api_requests.purchase_job_seeker(
            company_user_client,
            job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        data = resp.json()
        assert 'phone' in data
        assert 'email' in data['user']
        assert 'address' in data

    @pytest.mark.parametrize(('client',), (
        ('company_user_client',), ('company_user_2_client',)
    ))
    def test_purchase_saved_job_seeker_profile_move_from_saved_to_purchased(
            self, request, client, company_user_client, saved_job_seeker):
        client = request.getfixturevalue(client)
        resp = api_requests.purchase_job_seeker(client, saved_job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK

        query_params = {
            'saved': True
        }
        resp = api_requests.get_job_seekers(
            company_user_client,
            query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 0


class TestPurchaseJobSeekerValidate:

    def test_purchase_purchased_job_seeker(
            self, company_user_client, job_seeker):
        resp = api_requests.purchase_job_seeker(
            company_user_client,
            job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK

        resp = api_requests.purchase_job_seeker(
            company_user_client,
            job_seeker.id)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST
        emsg = company_constants.JOB_SEEKER_ALREADY_PURCHASED_ERROR
        validators.validate_error_message(resp, emsg)

    def test_purchase_applied_job_seeker(
            self, company_user_client, job_seeker, apply):
        resp = api_requests.purchase_job_seeker(
            company_user_client,
            job_seeker.id)
        data = resp.json()
        assert resp.status_code == http.HTTPStatus.OK
        assert 'phone' in data
        assert 'email' in data['user']
        assert 'address' in data
        assert data['is_purchased']

    def test_purchase_hidden_job_seeker(
            self, company_user_client, job_seeker_hidden):
        resp = api_requests.purchase_job_seeker(
            company_user_client,
            job_seeker_hidden.id)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST
        emsg = company_constants.PROFILE_IS_HIDDEN_ERROR
        validators.validate_error_message(resp, emsg)

    def test_purchase_job_seeker_fails_if_no_balance_left(
            self, company_user_client, job_seeker, company):
        company.customer.balance.job_seekers_remain = 0
        company.customer.balance.save()
        resp = api_requests.purchase_job_seeker(
            company_user_client,
            job_seeker.id)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST
        emsg = company_constants.OUT_OF_PROFILE_VIEWS_ERROR
        validators.validate_error_message(resp, emsg)
