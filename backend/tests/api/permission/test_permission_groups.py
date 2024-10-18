import http

import pytest

from tests import api_requests


class TestJobApiPermissions:

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
    def test_job_list(self, request, client, status):
        client = request.getfixturevalue(client)
        resp = api_requests.get_permissions_groups(client)
        assert resp.status_code == status


class TestJobApiInitialPermissions:

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
    def test_job_list(self, request, client, status):
        client = request.getfixturevalue(client)
        resp = api_requests.get_initial_permissions_groups(client)
        assert resp.status_code == status
