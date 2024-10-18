import http

import pytest

from survey import constants
from tests import api_requests


class TestDefaultQuestions:

    def test_get_default_questions(self, company_user_client):
        resp = api_requests.get_default_questions(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        data = resp.json()['results']
        for act, exp in zip(data, constants.DEFAULT_QUESTIONS):
            assert act['body'] == exp


class TestDefaultQuestionsPermissions:

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
    def test_get_default_questions(
            self, request, client, status):
        client = request.getfixturevalue(client)
        resp = api_requests.get_default_questions(client)
        assert resp.status_code == status
