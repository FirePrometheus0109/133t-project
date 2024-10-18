import http

import pytest

from job import models
from job_seeker import constants as js_constants
from public_api import constants
from tests import api_requests
from tests import utils
from tests import validators
from tests.api.public_api import expected


def test_get_enums(anonym_client):
    resp = api_requests.get_enums(anonym_client)
    assert resp.status_code == http.HTTPStatus.OK


def test_get_ini_settings(anonym_client):
    resp = api_requests.get_ini_settings(anonym_client)
    assert resp.status_code == http.HTTPStatus.OK


class TestPublicJobList:

    def test_get_public_job_list(self, anonym_client, all_published_jobs):
        resp = api_requests.get_job_list_unauthorized(anonym_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == len(all_published_jobs)


class TestBannedPublicJob:

    def test_banned_job_not_in_public_list(self, anonym_client,
                                           job_obj):
        resp = api_requests.get_job_list_unauthorized(anonym_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 1

        utils.ban_entity(job_obj)
        resp = api_requests.get_job_list_unauthorized(anonym_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 0

    def test_forbidden_retrieve_banned_job(self, anonym_client, job_obj):
        utils.ban_entity(job_obj)
        resp = api_requests.get_job_unauthorized(anonym_client, job_obj.id)
        assert resp.status_code == http.HTTPStatus.NOT_FOUND


class TestPublicJobSeeker:

    def test_get_shared_job_seeker_profile_success(
            self, anonym_client, shared_job_seeker):
        resp = api_requests.get_job_seeker_public(
            anonym_client, shared_job_seeker.guid)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json() == expected.EXPECTED_JS_PROFILE

    def test_get_shared_seeker__with_hidden_profile_fails(
            self, anonym_client, job_seeker_hidden,
            shared_job_seeker):
        resp = api_requests.get_job_seeker_public(
            anonym_client, shared_job_seeker.guid)
        validators.validate_error_message(
            resp,
            js_constants.PROFILE_IS_HIDDEN_ERROR,
            error_code=http.HTTPStatus.FORBIDDEN
        )

    def test_get_shared_job_seeker_with_nonshared_profile_fails(
            self, anonym_client, job_seeker):
        resp = api_requests.get_job_seeker_public(
            anonym_client, job_seeker.guid)
        validators.validate_error_message(
            resp,
            constants.PROFILE_IS_NOT_AVAILABLE_ERROR,
            error_code=http.HTTPStatus.FORBIDDEN
        )


class TestPublicJob:
    @pytest.mark.parametrize(('client',), (
            (
                    'anonym_client',
            ),
            (
                    'job_seeker_client',
            ),
            (
                    'company_user_client',
            ),
    ))
    def test_get_job_success(
            self, request, client, job_with_questions):
        client = request.getfixturevalue(client)
        job_obj = models.Job.objects.get(id=job_with_questions['id'])
        resp = api_requests.get_shared_job(client, job_obj.guid)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json() == expected.EXPECTED_JOB
