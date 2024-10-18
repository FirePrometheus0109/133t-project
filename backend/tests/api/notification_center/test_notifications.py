import copy
import datetime
import http
from unittest import mock

import pytest
from dateutil import relativedelta
from django.conf import settings
from django.utils import timezone

from apply import tasks as apply_tasks
from leet import enums
from subscription import tasks as s_tasks
from tests import api_requests
from tests.api.notification_center import expected


class TestListNotifications:

    @pytest.mark.parametrize(('fixture', 'api_request', 'exp'), (
        (
            'finished_autoapply',
            api_requests.get_short_notifications,
            expected.EXPECTED_NOTIFICATIONS_SHORT_AFTER_FINISHED_AUTOAPPLY
        ),
        (
            'finished_autoapply',
            api_requests.get_notifications,
            expected.EXPECTED_NOTIFICATIONS_AFTER_FINISHED_AUTOAPPLY
        ),
    ))
    def test_get_list_notifications_autoapply_action(
            self, job_seeker_client, request, fixture, api_request, exp):
        request.getfixturevalue(fixture)
        apply_tasks.send_autoapply_web_notifications.delay()
        resp = api_request(job_seeker_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json() == exp

    def test_get_list_short_notifications_only_unreaded_notifications(
            self, finished_autoapply, job_seeker_client):
        apply_tasks.send_autoapply_web_notifications.delay()
        resp = api_requests.get_short_notifications(job_seeker_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()
        resp = api_requests.get_short_notifications(job_seeker_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert not resp.json()

    def test_get_list_autoapply_short_notfications_notifications_are_disbled(
            self, finished_autoapply, js_client_no_subscribed_notifs):
        apply_tasks.send_autoapply_web_notifications.delay()
        resp = api_requests.get_short_notifications(
            js_client_no_subscribed_notifs)
        assert resp.status_code == http.HTTPStatus.OK
        assert not resp.json()

    def get_short_notifications_by_anonym(
            self, anonym_client, finished_autoapply):
        apply_tasks.send_autoapply_web_notifications.delay()
        resp = api_requests.get_short_notifications(anonym_client)
        assert resp.status_code == http.HTTPStatus.UNAUTHORIZED

    @pytest.mark.parametrize(('api_request', 'exp'), (
        (
            api_requests.get_short_notifications,
            [],
        ),
        (
            api_requests.get_notifications,
            {
                'count': 0,
                'next': None,
                'previous': None,
                'results': []
            }
        )
    ))
    def test_old_notifications_do_not_view_when_user_was_unscribed(
            self, js_client_no_subscribed_notifs, finished_autoapply,
            available_manage_notifications, api_request, exp):
        data = {'notification_types': []}
        for format_ in available_manage_notifications.values():
            for i in format_:
                data['notification_types'].append(i['id'])
        resp = api_requests.manage_notifications(
            js_client_no_subscribed_notifs, data)
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_request(js_client_no_subscribed_notifs)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json() == exp

    @pytest.mark.parametrize(
        ('api_request', 'exp', 'event_fixture', 'exp_timezone', 'check_timezone'),
        (
                (
                        api_requests.get_short_notifications,
                        expected.EXPECTED_NOTIF_SHORT_EVENT_INVITATION,
                        'event_in_est',
                        '',
                        False
                ),
                (
                        api_requests.get_notifications,
                        expected.EXPECTED_NOTIF_FULL_EVENT_INVITATION,
                        'event_in_est',
                        'EST',
                        True
                ),
                (
                        api_requests.get_notifications,
                        expected.EXPECTED_NOTIF_FULL_EVENT_INVITATION,
                        'event_in_edt',
                        'EDT',
                        True
                ),
        ))
    def test_get_notifications_after_creating_event(
            self, request, job_seeker_client, event_fixture,
            api_request, exp, exp_timezone, check_timezone):
        request.getfixturevalue(event_fixture)
        resp = api_request(job_seeker_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json() == exp
        if check_timezone:
            assert (resp.json()['results'][0]['data']['event']['timezone']
                    == exp_timezone)

    @pytest.mark.parametrize(('api_request', 'exp'), (
        (
            api_requests.get_short_notifications,
            expected.EXPECTED_NOTIF_SHORT_EVENT_UPDATED_INVITATION
        ),
        (
            api_requests.get_notifications,
            expected.EXPECTED_NOTIF_FULL_EVENT_UPDATED_INVITATION
        ),
    ))
    def test_get_notifications_after_updating_event(
            self, job_seeker_client, company_user_client,
            event_data, event, api_request, exp):
        data = copy.deepcopy(event_data)
        data['description'] = 'new unique description'
        resp = api_requests.update_event(
            company_user_client,
            event['id'],
            data
        )
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_request(job_seeker_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json() == exp

    @pytest.mark.parametrize(('api_request', 'exp'), (
        (
            api_requests.get_short_notifications,
            expected.EXPECTED_NOTIF_SHORT_EVENT_CANCELLED_INVITATION
        ),
        (
            api_requests.get_notifications,
            expected.EXPECTED_NOTIF_FULL_EVENT_CANCELLED_INVITATION
        ),
    ))
    def test_get_notifications_after_cancelling_event(
            self, job_seeker_client, company_user_client,
            event, api_request, exp):
        resp = api_requests.delete_event(
            company_user_client,
            event['id']
        )
        assert resp.status_code == http.HTTPStatus.NO_CONTENT
        resp = api_request(job_seeker_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json() == exp


class TestCompanyUserNotifications:

    @pytest.mark.parametrize(('api_request', 'exp'), (
        (
            api_requests.get_short_notifications,
            expected.EXPECTED_NOTIFS_COMPANY_USER_SHORT_END_OF_TRIAL
        ),
        (
            api_requests.get_notifications,
            expected.EXPECTED_NOTIFS_COMPANY_USER_FULL_END_OF_TRIAL
        )
    ))
    def test_send_notification_end_trial(
            self, mock_date, company_user_client, api_request, exp):
        period = settings.TRIAL_PERIOD_LENGTH - 5
        notif_date = timezone.now() + datetime.timedelta(days=period)
        with mock.patch('django.utils.timezone.now', new=lambda: notif_date):
            s_tasks.send_trial_expiration_notifications.delay()
            resp = api_request(company_user_client)
            assert resp.status_code == http.HTTPStatus.OK
            assert resp.json() == exp

    @pytest.mark.parametrize(('api_request', 'exp'), (
            (
                    api_requests.get_short_notifications,
                    expected.EXPECTED_NOTIFS_COMPANY_USER_SHORT_PACKAGE_DELETED
            ),
            (
                    api_requests.get_notifications,
                    expected.EXPECTED_NOTIFS_COMPANY_USER_FULL_PACKAGE_DELETED
            )
    ))
    def test_send_notification_package_deleted(
            self, company_user_client, subscription,
            deleted_corporate_package_50, api_request, exp):
        deletion_period_months = settings.MONTHS_COUNT_BEFORE_PLAN_CHANGES_APPLY
        deleted_corporate_package_50.deletion_date = (
                timezone.now()
                - relativedelta.relativedelta(months=deletion_period_months)
        )
        deleted_corporate_package_50.save()
        s_tasks.delete_subscription_plans.delay()
        resp = api_request(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json() == exp

    @pytest.mark.parametrize(('api_request', 'exp'), (
        (
            api_requests.get_short_notifications,
            expected.EXPECTED_NOTIF_SHORT_EVENT_RESPONSE_INVITATION
        ),
        (
            api_requests.get_notifications,
            expected.EXPECTED_NOTIF_FULL_EVENT_RESPONSE_INVITATION
        ),
    ))
    def test_get_notifications_after_event_response(
            self, job_seeker_client, company_user_client,
            event, api_request, exp):
        data = {'status': enums.EventAttendeeStatusEnum.ACCEPTED.name}
        resp = api_requests.change_attendee_status(
            job_seeker_client,
            event['candidates'][0]['id'],
            data
        )
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_request(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json() == exp
