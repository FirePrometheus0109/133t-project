import copy
import datetime
import http

import pytest
import pytz

from tests import api_requests
from tests import utils


@pytest.fixture
def today(tz_new_york):
    tz = pytz.timezone(tz_new_york)
    return datetime.datetime.now(tz=tz)


@pytest.fixture
def today_time_from(today):
    return datetime.datetime(
        today.year, today.month, today.day, 10, 0, tzinfo=today.tzinfo)


@pytest.fixture
def today_time_to(today):
    return datetime.datetime(
        today.year, today.month, today.day, 11, 0, tzinfo=today.tzinfo)


@pytest.fixture
def time_from_est(tz_new_york):
    dt = datetime.datetime(2019, 1, 15, 10, 0)
    return pytz.timezone(tz_new_york).localize(dt)


@pytest.fixture
def time_to_est(tz_new_york):
    dt = datetime.datetime(2019, 1, 15, 11, 0)
    return pytz.timezone(tz_new_york).localize(dt)


@pytest.fixture
def time_from_edt(tz_new_york):
    dt = datetime.datetime(2019, 6, 15, 10, 0)
    return pytz.timezone(tz_new_york).localize(dt)


@pytest.fixture
def time_to_edt(tz_new_york):
    dt = datetime.datetime(2019, 6, 15, 11, 0)
    return pytz.timezone(tz_new_york).localize(dt)


@pytest.fixture
def event_base_data(
        company_user, event_interview, today_time_from, today_time_to,
        country_usa, tz_new_york, city_new_york, zip_new_york):
    return {
        'colleagues': [company_user.user.id],
        'type': event_interview['id'],
        'location': {
            'address': 'address',
            'country': country_usa.id,
            'city': city_new_york.id,
            'zip': zip_new_york.id
        },
        'timezone': tz_new_york,
        'time_from': today_time_from.isoformat(),
        'time_to': today_time_to.isoformat(),
        'subject': 'subject',
        'description': 'description'
    }


@pytest.fixture
def candidate_one(company_user_client, job, purchased_job_seeker):
    return utils.create_candidate(
        company_user_client,
        job,
        purchased_job_seeker
    )


@pytest.fixture
def event_data(event_base_data, candidate_one):
    event_base_data['job'] = candidate_one['job']['id']
    event_base_data['candidates'] = [candidate_one['job_seeker']['user']['id']]
    return event_base_data


@pytest.fixture
def event(event_data, company_user_client):
    resp = api_requests.create_event(company_user_client, event_data)
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()


@pytest.fixture
def event_in_est(event_data, company_user_client,
                 time_from_est, time_to_est):
    data = copy.deepcopy(event_data)
    data['time_from'] = time_from_est.isoformat()
    data['time_to'] = time_to_est.isoformat()
    resp = api_requests.create_event(company_user_client, data)
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()


@pytest.fixture
def event_in_edt(event_data, company_user_client,
                 time_from_edt, time_to_edt):
    data = copy.deepcopy(event_data)
    data['time_from'] = time_from_edt.isoformat()
    data['time_to'] = time_to_edt.isoformat()
    resp = api_requests.create_event(company_user_client, data)
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()
