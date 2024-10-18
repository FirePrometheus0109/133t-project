import http

import pytest

from tests import api_requests


class TestViewedScoreCards:

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
    def test_manage_candidate_statuses_permission(
            self, request, client, status):
        data = {'statuses': []}
        client = request.getfixturevalue(client)
        resp = api_requests.manage_viewed_candidate_statuses(client, data)
        assert resp.status_code == status

    def test_view_all_scorecards(
            self, company_user_client, candidate_statuses):
        data = {'statuses': [i['id'] for i in candidate_statuses]}
        resp = api_requests.manage_viewed_candidate_statuses(
            company_user_client, data)
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()) == len(candidate_statuses)

    def test_hidded_all_scorecards(
            self, company_user_client, candidate_statuses):
        data = {'statuses': []}
        resp = api_requests.manage_viewed_candidate_statuses(
            company_user_client, data)
        assert resp.status_code == http.HTTPStatus.OK
        assert not resp.json()

    def test_hidded_all_scorecard_excelude_applied(
            self, company_user_client, cand_status_applied):
        data = {'statuses': [cand_status_applied['id']]}
        resp = api_requests.manage_viewed_candidate_statuses(
            company_user_client, data)
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()) == 1
        assert resp.json()[0]['name'] == cand_status_applied['name']
