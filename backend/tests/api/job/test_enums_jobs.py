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
    def test_get_job_enums_permissions(
            self, request, client, status):
        client = request.getfixturevalue(client)
        resp = api_requests.get_job_enums(client)
        assert resp.status_code == status
