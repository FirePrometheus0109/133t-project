import http

import pytest

from tests import api_requests


class TestCandidateEnums:

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
    def test_get_candidate_enums_permissions(
            self, request, client, status):
        client = request.getfixturevalue(client)
        resp = api_requests.get_candidates_enums(client)
        assert resp.status_code == status

    @pytest.mark.parametrize(('fixture', 'count'), (
        (
            'job',
            0
        ),
        (
            'job1',
            1
        )
    ))
    def test_get_candidate_enums(
            self, request, company_user_client, apply, fixture, count):
        job = request.getfixturevalue(fixture)
        query_params = {'job': job['id']}
        resp = api_requests.get_candidates_enums(
            company_user_client,
            query_params=query_params
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()) == count
