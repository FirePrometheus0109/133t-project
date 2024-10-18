import copy
import http

import pytest

from apply import tasks
from tests import api_requests
from tests import utils


@pytest.fixture
def available_manage_notifications(job_seeker_client):
    resp = api_requests.get_notification_types(job_seeker_client)
    assert resp.status_code == http.HTTPStatus.OK
    return resp.json()


@pytest.fixture
def js_client_no_subscribed_notifs(job_seeker_client):
    data = {'notification_types': []}
    resp = api_requests.manage_notifications(job_seeker_client, data)
    assert resp.status_code == http.HTTPStatus.OK
    return job_seeker_client


@pytest.fixture
def finished_autoapply(
        job_seeker_client, started_autoapply, autoapply_base_data):
    data = copy.deepcopy(autoapply_base_data)
    data['number'] = 1
    resp = api_requests.update_autoapply(
        job_seeker_client,
        started_autoapply['id'],
        data)
    assert resp.status_code == http.HTTPStatus.OK
    tasks.find_autoapply_jobs.delay()
    return started_autoapply


@pytest.fixture
def autoapply_new_jobs(started_autoapply, job1):
    tasks.find_autoapply_jobs.delay()
    return started_autoapply


@pytest.fixture
def mock_date(mocker):
    """
    This fixture used for test test_send_notification_end_trial
    For correct checking dates. Subscription ends on 24 February
    """
    date = utils.date(2019, 2, 7)
    fixture = mocker.patch('django.utils.timezone.now', new=lambda: date)
    return fixture()
