import datetime
import http
from unittest import mock

import pytest
from django.conf import settings
from django.utils import timezone

from tests import api_requests


class TestQuickList:

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.FORBIDDEN
        ),
        (
            'company_user_client',
            http.HTTPStatus.OK
        ),
    ))
    def test_get_quick_list_permissions(self, request, client, status):
        client = request.getfixturevalue(client)
        resp = api_requests.get_quick_list(client)
        assert resp.status_code == status

    @pytest.mark.parametrize(('fixture', 'count'), (
        (
            'cand_status_rejected',
            1,
        ),
        (
            'cand_status_applied',
            0
        )
    ))
    def test_get_quick_list_filter_by_status(
            self, request, rejected_candidate,
            company_user_client, fixture, count):
        status = request.getfixturevalue(fixture)
        query_params = {'status': status['id']}
        resp = api_requests.get_quick_list(
            company_user_client,
            query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()) == count

    @pytest.mark.parametrize(('value', 'count'), (
        (
            'jsfirstname',
            1
        ),
        (
            'jp1',
            1
        ),
        (
            'nomatch',
            0
        ),
        (
            'name',
            1
        )
    ))
    def test_search_candidates_in_quick_list(
            self, company_user_client, assigned_candidate, value, count):
        query_params = {'search': value}
        resp = api_requests.get_quick_list(
            company_user_client,
            query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()) == count

    @pytest.mark.parametrize(('client', 'count'), (
        (
            'company_user_client',
            1
        ),
        (
            'company_user_2_client',
            0
        )
    ))
    def test_get_quick_list_for_owner(
            self, request, client, rejected_candidate, count):
        client = request.getfixturevalue(client)
        resp = api_requests.get_quick_list(client)
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()) == count

    @pytest.mark.parametrize(('fixture',), (
        (
            'candidate_screened',
        ),
        (
            'candidate_viewed_details',
        ),
        (
            'candidate_viewed_js_profile',
        ),
        (
            'candidate_viewed_quick_list',
        ),
        (
            'candidate_commented',
        )
    ))
    def test_get_quick_list_actions_during_5_days(
            self, company_user_client, request, fixture):
        request.getfixturevalue(fixture)
        n_days = settings.NUMBER_DAYS_FOR_QUICK_LIST
        mock_date = timezone.now() + datetime.timedelta(days=n_days)
        with mock.patch('django.utils.timezone.now', new=lambda: mock_date):
            resp = api_requests.get_quick_list(company_user_client)
            assert resp.status_code == http.HTTPStatus.OK
            assert len(resp.json()) == 1
        # after 5 days
        mock_date += datetime.timedelta(days=1)
        with mock.patch('django.utils.timezone.now', new=lambda: mock_date):
            resp = api_requests.get_quick_list(company_user_client)
            assert resp.status_code == http.HTTPStatus.OK
            assert len(resp.json()) == 0

    def test_get_quick_list_actions_view_job_seeker_details_no_candidate(
            self, company_user_client, job_seeker):
        resp = api_requests.get_job_seeker_details(
            company_user_client,
            job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_requests.get_quick_list(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()) == 0

    def test_qucik_list_assigned_candidate_changed_steps(
            self, company_user_client, job_seeker, cand_status_screened,
            cand_status_rejected, assigned_candidate):
        data = {'status': cand_status_screened['id']}
        resp = api_requests.update_candidate_status(
            company_user_client,
            assigned_candidate['id'],
            data,
        )
        assert resp.status_code == http.HTTPStatus.OK
        data = {'status': cand_status_rejected['id']}
        resp = api_requests.update_candidate_status(
            company_user_client,
            assigned_candidate['id'],
            data
        )
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_requests.get_quick_list(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()) == 1

    def test_quick_list_assigned_candidate_view(
            self, company_user_client, assigned_candidate):
        resp = api_requests.get_candidate(
            company_user_client,
            assigned_candidate['id']
        )
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_requests.get_job_seeker_details(
            company_user_client,
            assigned_candidate['job_seeker']['id']
        )
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_requests.get_candidate_quick_view(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_requests.get_quick_list(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()) == 1

    def test_quick_list_more_recently_worked_with_first(
            self, company_user_client, purchased_job_seekers, job):
        data = {
            'jobs': [job['id']],
            'job_seekers': [js.id for js in purchased_job_seekers]
        }
        resp = api_requests.assign_candidate_to_job(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.CREATED
        resp = api_requests.get_candidates(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 2
        candidate_1 = resp.json()['results'][0]
        candidate_2 = resp.json()['results'][1]

        resp = api_requests.get_candidate(
            company_user_client,
            candidate_2['id']
        )
        assert resp.status_code == http.HTTPStatus.OK

        resp = api_requests.get_candidate(
            company_user_client,
            candidate_1['id']
        )
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_requests.get_quick_list(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()) == 2
        # first in the list should be candidate_1 because company user
        # worked with this candidate more recently
        assert resp.json()[0]['id'] == candidate_1['id']
        resp = api_requests.get_candidate(
            company_user_client,
            candidate_2['id']
        )
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_requests.get_quick_list(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()) == 2
        assert resp.json()[0]['id'] == candidate_2['id']
