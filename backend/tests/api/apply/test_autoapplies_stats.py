import http

import pytest

from apply import tasks
from tests import api_requests
from tests.api.apply import expected


class TestAutoAppliesStats:

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED,
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.OK,
        ),
        (
            'company_user_client',
            http.HTTPStatus.FORBIDDEN,
        ),
    ))
    def test_get_autoapplies_stats_permissions(self, request, client, status):
        client = request.getfixturevalue(client)
        resp = api_requests.get_autoapplies_stats(client)
        assert resp.status_code == status

    def test_get_autoapplies_stats(
            self, job_seeker_client, job_seeker_autoapplies):
        tasks.find_autoapply_jobs.delay()
        resp = api_requests.get_autoapplies_stats(job_seeker_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json() == expected.EXPECTED_AUTOAPPLIES_STATS
