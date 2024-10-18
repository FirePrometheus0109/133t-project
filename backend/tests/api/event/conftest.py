import copy
import http

import pytest

from leet import enums
from tests import api_requests
from tests import utils


@pytest.fixture
def candidate_two(company_user_client, job, purchased_job_seeker_2):
    return utils.create_candidate(
        company_user_client,
        job,
        purchased_job_seeker_2
    )


@pytest.fixture
def candidate_three(company_user_client, job, purchased_job_seeker_3):
    return utils.create_candidate(
        company_user_client,
        job,
        purchased_job_seeker_3
    )


@pytest.fixture
def candidates_one_and_two(candidate_one, candidate_two):
    return [candidate_one, candidate_two]


@pytest.fixture
def event_two_candidates(
        company_user_client, event_base_data, candidates_one_and_two):
    data = copy.deepcopy(event_base_data)
    data['candidates'] = [
        i['job_seeker']['user']['id'] for i in candidates_one_and_two
    ]
    data['job'] = candidates_one_and_two[0]['job']['id']
    resp = api_requests.create_event(company_user_client, data)
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()


@pytest.fixture
def attendee_candidate(event):
    return event['candidates'][0]


@pytest.fixture
def attendee_candidate_accepted(attendee_candidate, job_seeker_client):
    data = {'status': enums.EventAttendeeStatusEnum.ACCEPTED.name}
    resp = api_requests.change_attendee_status(
        job_seeker_client,
        attendee_candidate['id'],
        data
    )
    assert resp.status_code == http.HTTPStatus.OK
    return attendee_candidate
