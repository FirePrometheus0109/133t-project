import http

import pytest

from tests import api_requests
from tests.api.candidate import expected
from tests.utils import Any, ban_entity


class TestCandidateQuickView:

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
        (
            'company_2_user_client',
            http.HTTPStatus.OK
        ),
        (
            'company_user_2_client',
            http.HTTPStatus.OK
        ),
    ))
    def test_get_candidate_quick_view(
            self, request, client, status, company_user_candidate_1):
        client = request.getfixturevalue(client)
        resp = api_requests.get_candidate_quick_view(client)
        assert resp.status_code == status

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'company_user_client',
            http.HTTPStatus.OK,
        ),
        (
            'company_user_2_client',
            http.HTTPStatus.OK,
        )
    ))
    def test_get_candidates_available_for_all_company_mates(
            self, company_user_candidate_1, request, client, status):
        client = request.getfixturevalue(client)
        resp = api_requests.get_candidate_quick_view(client)
        assert resp.status_code == status

    @pytest.mark.parametrize(('client', 'status', 'results_count'), (
        (
            'company_user_client',
            http.HTTPStatus.OK,
            1
        ),
        (
            'company_2_user_client',
            http.HTTPStatus.OK,
            0
        )
    ))
    def test_company_users_can_see_candidates_from_different_jobs(
            self, company_user_candidate_1, request, client, status,
            results_count):
        client = request.getfixturevalue(client)
        resp = api_requests.get_candidate_quick_view(client)
        assert resp.status_code == status
        assert resp.json()['count'] == results_count

    def test_candidate_quick_view_max_limit(
            self, company_user_client, company_user_candidates):
        query_params = {'limit': 777}
        resp = api_requests.get_candidate_quick_view(company_user_client,
                                                     query_params)
        assert resp.status_code == http.HTTPStatus.OK
        resp_data = resp.json()
        assert resp_data['count'] == len(company_user_candidates)
        assert len(resp_data['results']) == expected.QUICK_VIEW_RESULTS_LIMIT
        assert resp_data['next'] == Any(str)

    def test_banned_candidate_not_in_quick_view(
            self, company_user_client, company_user_candidates):
        resp = api_requests.get_candidate_quick_view(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == len(company_user_candidates)

        ban_entity(company_user_candidates[0].job_seeker)
        resp = api_requests.get_candidate_quick_view(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == len(company_user_candidates) - 1
