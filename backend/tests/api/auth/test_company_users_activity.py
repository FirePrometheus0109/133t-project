import datetime
import http

import mock
import pytest
from django.conf import settings
from django.utils import timezone

from tests import api_requests
from tests.api.auth import expected


class TestCompanyUserActivity:

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
            'company_user_2_client',
            http.HTTPStatus.OK
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.FORBIDDEN
        )
    ))
    def test_get_company_users_activity(
            self, request, client, status, company_user_client, company):
        client = request.getfixturevalue(client)
        resp = api_requests.get_company_users_activity(client, company.id)
        assert resp.status_code == status

    def test_company_user_online_status(
            self, company, company_user_client, active_company_user,
            company_user_2_creds, anonym_client):
        resp = api_requests.get_company_users_activity(
            company_user_client, company.id)
        assert resp.status_code == http.HTTPStatus.OK
        resp_data = resp.json()
        assert resp_data['count'] == 2
        assert resp_data['results'][0]['is_online']
        assert not resp_data['results'][1]['is_online']

        # make request to update `active_company_user` last activity
        resp = api_requests.login(anonym_client, company_user_2_creds)
        assert resp.status_code == http.HTTPStatus.OK

        resp = api_requests.get_company_users_activity(
            company_user_client, company.id)
        assert resp.status_code == http.HTTPStatus.OK
        resp_data = resp.json()
        assert resp_data['results'][0]['is_online']
        assert resp_data['results'][1]['is_online']

    def test_correct_online_status_for_company_user(
            self, company, company_user_client, company_user_2_client):
        resp = api_requests.get_company_users_activity(
            company_user_client, company.id)
        resp_data = resp.json()
        assert resp_data['results'][0]['is_online']
        assert resp_data['results'][1]['is_online']

        time_shift = timezone.now() + datetime.timedelta(
            minutes=settings.USER_CONSIDERED_ONLINE_TIME_DELTA + 1)
        with mock.patch('django.utils.timezone.now', new=lambda: time_shift):
            resp = api_requests.get_company_users_activity(
                company_user_client, company.id)
            assert resp.status_code == http.HTTPStatus.OK
            resp_data = resp.json()
            assert not resp_data['results'][0]['is_online']
            assert not resp_data['results'][1]['is_online']

    def test_company_users_report_activity_correct_data(
            self, company, company_user, company_user_2_client,
            company_user_client, rejected_candidate):
        resp = api_requests.get_company_users_activity(
            company_user_client, company.id)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['results'] == expected.COMPANY_USERS_REPORT_ACTIVITY

    def test_company_user_report_activity_should_return_all_statuses(
            self, company, company_user_client,
            rejected_candidate):
        data = {'statuses': []}
        resp = api_requests.manage_viewed_candidate_statuses(
            company_user_client, data)
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_requests.get_company_users_activity(
            company_user_client, company.id)
        assert resp.status_code == http.HTTPStatus.OK
        assert (resp.json()['results'] ==
                expected.COMPANY_USERS_REPORT_ACTIVITY_ONE_USER)
