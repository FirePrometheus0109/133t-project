import http

import pytest

from job_seeker import constants
from tests import api_requests
from tests import utils
from tests import validators


class TestSavedJobSeeker:

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
    def test_save_job_seeker(self, request, client, status, job_seeker,
                             save_job_seeker_data):
        client = request.getfixturevalue(client)
        resp = api_requests.save_remove_job_seeker(
            client, job_seeker.id, save_job_seeker_data)
        assert resp.status_code == status

    def test_save_job_seeker_success(
            self, company_user_client, job_seeker, save_job_seeker_data):
        resp = api_requests.save_remove_job_seeker(
            company_user_client, job_seeker.id, save_job_seeker_data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['saved_at']

    def test_remove_saved_job_seeker_success(
            self, company_user_client, job_seeker, saved_job_seeker,
            remove_job_seeker_data):
        resp = api_requests.save_remove_job_seeker(
            company_user_client, job_seeker.id, remove_job_seeker_data)
        assert resp.status_code == http.HTTPStatus.NO_CONTENT

    def test_remove_not_saved_job_seeker_success(
            self, company_user_client, job_seeker, remove_job_seeker_data):
        resp = api_requests.save_remove_job_seeker(
            company_user_client, job_seeker.id, remove_job_seeker_data)
        assert resp.status_code == http.HTTPStatus.NO_CONTENT

    def test_save_purchased_job_seeker_fail(
            self, company_user_client, job_seeker, purchased_job_seeker,
            save_job_seeker_data):
        resp = api_requests.save_remove_job_seeker(
            company_user_client, job_seeker.id, save_job_seeker_data)
        emsg = constants.SAVED_JOB_SEEKER_ALREADY_PURCHASED_ERROR.format(
            job_seeker.user.get_full_name())
        validators.validate_error_message(resp, emsg)

    def test_save_candidate_job_seeker_fail(
            self, company_user_client, job_seeker, candidate,
            save_job_seeker_data):
        resp = api_requests.save_remove_job_seeker(
            company_user_client, job_seeker.id, save_job_seeker_data)
        emsg = constants.SAVED_JOB_SEEKER_ALREADY_CANDIDATE_ERROR.format(
            job_seeker.user.get_full_name())
        validators.validate_error_message(resp, emsg)

    def test_save_banned_job_seeker_fail(
            self, company_user_client, job_seeker, save_job_seeker_data):
        utils.ban_entity(job_seeker)
        resp = api_requests.save_remove_job_seeker(
            company_user_client, job_seeker.id, save_job_seeker_data)
        emsg = constants.SAVED_JOB_SEEKER_BANNED_ERROR.format(
            job_seeker.user.get_full_name())
        validators.validate_error_message(resp, emsg)
