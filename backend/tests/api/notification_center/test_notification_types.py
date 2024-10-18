import http

from tests import api_requests
from tests.api.notification_center import expected


class TestNotificationTypes:

    def test_get_list_available_notification_types_for_manage(
            self, job_seeker_client):
        resp = api_requests.get_notification_types(job_seeker_client)
        assert resp.status_code == http.HTTPStatus.OK
        exp = expected.EXPECTED_LIST_AVAILABLE_TO_CHANGE_NOTIFICATION_TYPES
        assert resp.json() == exp
