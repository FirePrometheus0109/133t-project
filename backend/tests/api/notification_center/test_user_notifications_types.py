import http

import pytest

from notification_center import constants
from tests import api_requests
from tests.api.notification_center import expected


class TestUserNotificationTypes:

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.OK
        ),
        (
            'company_user_client',
            http.HTTPStatus.FORBIDDEN
        )
    ))
    def test_get_user_notification_types_permissions(
            self, request, client, status):
        client = request.getfixturevalue(client)
        resp = api_requests.get_user_notifications_types(client)
        assert resp.status_code == status

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.OK
        ),
        (
            'company_user_client',
            http.HTTPStatus.FORBIDDEN
        )
    ))
    def test_manage_user_notification_types_permissions(
            self, request, client, status):
        client = request.getfixturevalue(client)
        data = {'notification_types': []}
        resp = api_requests.manage_notifications(client, data)
        assert resp.status_code == status

    def test_get_user_notifications(self, job_seeker_client):
        resp = api_requests.get_user_notifications_types(job_seeker_client)
        assert resp.status_code == http.HTTPStatus.OK
        exp = expected.EXPECTED_LIST_AVAILABLE_TO_CHANGE_NOTIFICATION_TYPES
        assert resp.json() == exp

    def test_delete_all_available_user_notifications(self, job_seeker_client):
        data = {'notification_types': []}
        resp = api_requests.manage_notifications(
            job_seeker_client,
            data)
        assert resp.status_code == http.HTTPStatus.OK
        data = resp.json()
        assert not resp.json()[constants.NOTIFICATION_FORMAT_EMAIL]
        assert not resp.json()[constants.NOTIFICATION_FORMAT_WEB]

    def test_manage_notification_leave_one(
            self, job_seeker_client, available_manage_notifications):
        notif_format_email = constants.NOTIFICATION_FORMAT_EMAIL
        invitations_email_notif = next(
            i for i in available_manage_notifications[notif_format_email]
            if i['name'] == constants.NOTIFICATION_TYPE_INVITATION_RECEIVED
        )
        data = {'notification_types': [invitations_email_notif['id']]}
        resp = api_requests.manage_notifications(job_seeker_client, data)
        assert resp.status_code == http.HTTPStatus.OK
        data = resp.json()[notif_format_email]
        assert len(data) == 1
        assert data[0]['id'] == invitations_email_notif['id']
