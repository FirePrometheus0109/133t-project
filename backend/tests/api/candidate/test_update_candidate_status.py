import http

import pytest

from candidate import constants
from candidate import models
from tests import api_requests
from tests import validators


class TestUpdateCandidateStatus:

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
            'company_user_2_client',
            http.HTTPStatus.OK
        ),
        (
            'company_2_user_client',
            http.HTTPStatus.NOT_FOUND
        ),
    ))
    def test_update_candidate_status_access_api(
            self, request, client, status,
            company_user_candidate_1, candidate_status_data):
        client = request.getfixturevalue(client)
        resp = api_requests.update_candidate_status(
            client,
            company_user_candidate_1.id,
            candidate_status_data)

        assert resp.status_code == status

    def test_update_candidate_status_in_workflow(
            self, company_user, company_user_candidate_1,
            company_user_client, candidate_status_data,
            cand_status_applied):
        resp = api_requests.update_candidate_status(
            company_user_client,
            company_user_candidate_1.id,
            candidate_status_data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['id'] == candidate_status_data['status']
        assert company_user == models.WorkflowStep.objects.last().owner

    def test_update_status_rejected_candidate(
            self, rejected_candidate,
            company_user_client, candidate_status_data):
        resp = api_requests.update_candidate_status(
            company_user_client,
            rejected_candidate['id'],
            candidate_status_data)
        emsg = constants.NOT_VALID_CANDIDATE_FOR_CHANGE_STATUS
        validators.validate_error_message(resp, emsg)

    def test_company_with_starter_package_can_change_wf_status(
            self, company_user_client, company_user_candidate_1,
            candidate_status_data, starter_subscription):
        resp = api_requests.update_candidate_status(
            company_user_client,
            company_user_candidate_1.id,
            candidate_status_data)

        assert resp.status_code == http.HTTPStatus.OK
