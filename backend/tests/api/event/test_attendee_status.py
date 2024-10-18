import http

import pytest

from event import constants
from leet import enums
from tests import api_requests
from tests import validators


class TestAttendee:

    @pytest.mark.parametrize(('data', 'status_value'), (
        (
            {
                'status': enums.EventAttendeeStatusEnum.ACCEPTED.name
            },
            enums.EventAttendeeStatusEnum.ACCEPTED.name.lower()
        ),
        (
            {
                'status': enums.EventAttendeeStatusEnum.REJECTED.name
            },
            enums.EventAttendeeStatusEnum.REJECTED.name.lower()
        )
    ))
    def test_change_attendee_event_status(
            self, job_seeker_client, attendee_candidate,
            data, status_value, mailoutbox):
        mailoutbox.clear()
        resp = api_requests.change_attendee_status(
            job_seeker_client,
            attendee_candidate['id'],
            data
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['status'] == data['status']
        assert len(mailoutbox) == 1
        message = mailoutbox[0].message().as_string()
        assert status_value in message

    def test_change_attendee_status_invited(
            self, job_seeker_client, attendee_candidate, mailoutbox):
        mailoutbox.clear()
        data = {
            'status': enums.EventAttendeeStatusEnum.INVITED.name
        }
        resp = api_requests.change_attendee_status(
            job_seeker_client,
            attendee_candidate['id'],
            data
        )
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST
        assert len(mailoutbox) == 0

    def test_change_attendee_status_raises_if_event_was_responded(
            self, job_seeker_client, attendee_candidate_accepted, mailoutbox):
        mailoutbox.clear()
        data = {'status': enums.EventAttendeeStatusEnum.REJECTED.name}
        resp = api_requests.change_attendee_status(
            job_seeker_client,
            attendee_candidate_accepted['id'],
            data
        )
        validators.validate_error_message(
            resp, constants.ATTENDEE_HAS_ALREADY_RESPONDED, 'status'
        )
        assert len(mailoutbox) == 0
