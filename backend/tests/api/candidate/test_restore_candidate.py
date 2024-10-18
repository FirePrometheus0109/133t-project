import copy
import http

import pytest

from candidate import constants
from leet import enums
from tests import api_requests
from tests import validators


class TestRestoreCandidate:

    def test_restore_rejected_candidate_candidate_is_not_rejected(
            self, candidate, company_user_client):
        resp = api_requests.restore_candidate(
            company_user_client,
            candidate['id'])
        emsg = constants.RESTORE_CANDIDATE_ERROR
        validators.validate_error_message(resp, emsg)

    def test_reject_candidate(
            self, candidate, company_user_client,
            cand_status_rejected):
        data = {'status': cand_status_rejected['id']}
        resp = api_requests.update_candidate_status(
            company_user_client,
            candidate['id'],
            data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['id'] == data['status']

    def test_restore_rejected_candidate(
            self, rejected_candidate,
            company_user_client, cand_status_applied):
        resp = api_requests.restore_candidate(
            company_user_client,
            rejected_candidate['id'])
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['id'] == cand_status_applied['id']

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
            http.HTTPStatus.NOT_FOUND
        ),
    ))
    def test_restore_candidate_permission(
            self, request, client, status, rejected_candidate):
        client = request.getfixturevalue(client)
        resp = api_requests.restore_candidate(
            client,
            rejected_candidate['id'])
        assert resp.status_code == status

    def test_restore_reapplied_candidate(
            self, job_seeker_client, company_user_client, rejected_candidate):
        resp = api_requests.reapply_for_job(
            job_seeker_client,
            rejected_candidate['job']['id'])
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_requests.restore_candidate(
            company_user_client,
            rejected_candidate['id'])
        emsg = constants.REJECTED_CANDIDATE_ALREADY_REAPPLIED_ERROR
        validators.validate_error_message(resp, emsg)

    def test_restore_rejected_candidate_job_closed(
            self, company_user_client, job1,
            job_base_data, rejected_candidate):
        data = copy.deepcopy(job_base_data)
        data['status'] = enums.JobStatusEnum.CLOSED.name
        resp = api_requests.update_job(company_user_client, job1['id'], data)
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_requests.restore_candidate(
            company_user_client,
            rejected_candidate['id']
        )
        emsg = constants.REJECTED_CANDIDATE_JOB_IS_CLOSED_ERROR
        validators.validate_error_message(resp, emsg)

    def test_restore_rejected_candidate_job_is_deleted(
            self, company_user_client, job1, rejected_candidate):
        resp = api_requests.delete_job(company_user_client, job1['id'])
        assert resp.status_code == http.HTTPStatus.NO_CONTENT
        resp = api_requests.restore_candidate(
            company_user_client,
            rejected_candidate['id']
        )
        emsg = constants.REJECTED_CANDIDATE_JOB_IS_DELETED_ERROR
        validators.validate_error_message(resp, emsg)
