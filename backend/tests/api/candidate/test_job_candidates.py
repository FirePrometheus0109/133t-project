import http

import pytest

from tests import api_requests


class TestJobCandidatesApi:

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
            'company_2_user_client',
            http.HTTPStatus.FORBIDDEN
        ),
        (
            'company_user_client',
            http.HTTPStatus.OK
        )
    ))
    def test_get_candidates_permissions(
            self, request, job, client, status):
        client = request.getfixturevalue(client)
        resp = api_requests.get_job_candidates(
            client,
            job['id'])
        assert resp.status_code == status

    def test_get_all_job_candidates(
            self, company_user_client, job1, job1_candidates):
        resp = api_requests.get_job_candidates(
            company_user_client,
            job1['id'])
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 2

    def test_get_job_candidates_by_status(
            self, company_user_client, job1,
            job1_candidates, cand_status_applied):
        filters = {'status': cand_status_applied['id']}
        resp = api_requests.get_job_candidates(
            company_user_client,
            job1['id'],
            filters=filters)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 2

    def test_get_job_candidates_no_candidates_with_certain_status(
            self, company_user_client, job1,
            job1_candidates, cand_status_rejected):
        filters = {'status': cand_status_rejected['id']}
        resp = api_requests.get_job_candidates(
            company_user_client,
            job1['id'],
            filters=filters)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 0

    @pytest.mark.parametrize(('status_fixture', 'expected_count'), (
        (
            'cand_status_rejected',
            1
        ),
        (
            'cand_status_applied',
            1
        ),
    ))
    def test_get_job_candidates_different_query_strings(
            self, company_user_client, request, job1, status_fixture,
            expected_count, job1_candidates, rejected_candidate):
        status = request.getfixturevalue(status_fixture)
        filters = {'status': status['id']}
        resp = api_requests.get_job_candidates(
            company_user_client,
            job1['id'],
            filters=filters)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == expected_count
