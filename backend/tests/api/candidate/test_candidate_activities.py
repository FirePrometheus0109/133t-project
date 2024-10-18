import http

import pytest

from tests import api_requests
from tests.api.candidate import expected


class TestAssignCandidateToJobPermissions:

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
    def test_get_candidates_activities_permissions(
            self, request, client, status):
        client = request.getfixturevalue(client)
        resp = api_requests.get_candidates_activities(client)
        assert resp.status_code == status

    @pytest.mark.parametrize(('candidate_fixture', 'exp'), (
        (
            'candidate',
            expected.EXPECTED_CANDIDATES_ACTIVITIES_AFTER_APPLY
        ),
        (
            'assigned_candidate',
            expected.EXPECTED_CANDIDATES_ACTIVITIES_AFTER_ASSIGN
        ),
    ))
    def test_get_candidates_activities(
            self, request, candidate_fixture, company_user_client, exp):
        request.getfixturevalue(candidate_fixture)
        resp = api_requests.get_candidates_activities(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['results'] == exp
