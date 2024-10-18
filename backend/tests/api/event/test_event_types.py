import http

import pytest

from tests import api_requests


class TestViewEventTypePermissions:

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
    def test_view_event_types_permissions(self, client, request, status):
        client = request.getfixturevalue(client)
        resp = api_requests.get_event_types(client)
        assert resp.status_code == status
