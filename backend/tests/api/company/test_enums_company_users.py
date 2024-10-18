import http

import pytest

from tests import api_requests


class TestCompanyUserEnums:

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
    def test_get_company_users_enums_permissions(
            self, request, client, status):
        client = request.getfixturevalue(client)
        resp = api_requests.get_company_users_enums(client)
        assert resp.status_code == status

    def test_get_company_users(self, company_user_client, active_company_user):
        resp = api_requests.get_company_users_enums(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()) == 2
