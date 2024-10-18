import datetime
import http

import pytest

from event import constants
from tests import api_requests


class TestAnotherEvent:

    @pytest.mark.parametrize(('query_params',), (
        (
            {
                'time_from': datetime.datetime(2019, 1, 1, 10, 0).isoformat()
            },
        ),
        (
            {
                'time_to': datetime.datetime(2019, 1, 1, 10, 0).isoformat()
            },
        )
    ))
    def test_check_another_events_no_required_params(
            self, company_user_client, query_params):
        resp = api_requests.check_another_events(
            company_user_client,
            query_params
        )
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST

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
    def test_check_another_events_permissions(
            self, client, request, status):
        client = request.getfixturevalue(client)
        query_params = {
            'time_from': datetime.datetime(2019, 1, 1, 9, 0).isoformat(),
            'time_to': datetime.datetime(2019, 1, 1, 10, 0).isoformat(),
        }
        resp = api_requests.check_another_events(client, query_params)
        assert resp.status_code == status

    @pytest.mark.parametrize(('time_from', 'time_to', 'msg'), (
        # event has time_from 10:00, time_to 11:00, date today,
        # see event conftest
        (
            datetime.time(9, 0),
            datetime.time(9, 30),
            ''
        ),
        (
            datetime.time(12, 0),
            datetime.time(13, 30),
            ''
        ),
        (
            datetime.time(9, 0),
            datetime.time(13, 30),
            constants.ANOTHER_EVENT_AT_THE_SAME_TIME_MESSAGE
        ),
        (
            datetime.time(9, 30),
            datetime.time(10, 30),
            constants.ANOTHER_EVENT_AT_THE_SAME_TIME_MESSAGE
        ),
        (
            datetime.time(9, 0),
            datetime.time(10, 0),
            ''
        ),
        (
            datetime.time(11, 0),
            datetime.time(12, 0),
            ''
        ),
    ))
    def test_check_another_events(
            self, company_user_client, time_from, time_to, event, msg, today):
        time_from = datetime.datetime(
            today.year,
            today.month,
            today.day,
            time_from.hour,
            time_from.minute,
            tzinfo=today.tzinfo)
        time_to = datetime.datetime(
            today.year,
            today.month,
            today.day,
            time_to.hour,
            time_to.minute,
            tzinfo=today.tzinfo)
        query_params = {
            'time_from': time_from.isoformat(),
            'time_to': time_to.isoformat(),
        }
        resp = api_requests.check_another_events(
            company_user_client,
            query_params
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['message'] == msg

    @pytest.mark.parametrize(('time_from', 'time_to'), (
        # event has time_from 10:00, time_to 11:00, date today,
        # see event conftest
        (
            datetime.time(9, 30),
            datetime.time(10, 0),
        ),
        (
            datetime.time(9, 30),
            datetime.time(10, 30),
        ),
        (
            datetime.time(10, 30),
            datetime.time(11, 30),
        ),
        (
            datetime.time(11, 0),
            datetime.time(12, 0),
        ),
    ))
    def test_check_another_events_exludes_current_event_from_check(
            self, company_user_client, time_from, time_to, event, today):
        time_from = datetime.datetime(
            today.year,
            today.month,
            today.day,
            time_from.hour,
            time_from.minute,
            tzinfo=today.tzinfo)
        time_to = datetime.datetime(
            today.year,
            today.month,
            today.day,
            time_to.hour,
            time_to.minute,
            tzinfo=today.tzinfo)
        query_params = {
            'time_from': time_from.isoformat(),
            'time_to': time_to.isoformat(),
            'id': event['id']
        }
        resp = api_requests.check_another_events(
            company_user_client,
            query_params
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert not resp.json()['message']
