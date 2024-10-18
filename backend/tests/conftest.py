import datetime
import http

import pytest
from django.utils import timezone

from leet import constants
from tests import api_requests
from tests import test_data

pytest_plugins = (
    'tests.fixtures.clients',
    'tests.fixtures.geo',
    'tests.fixtures.job_seeker',
    'tests.fixtures.company',
    'tests.fixtures.job',
    'tests.fixtures.apply',
    'tests.fixtures.survey',
    'tests.fixtures.candidate',
    'tests.fixtures.admin',
    'tests.fixtures.comments',
    'tests.fixtures.subscription',
    'tests.fixtures.event',
)


@pytest.fixture
def mock_send_email_confirm(mocker):
    mockname = 'allauth.account.utils.send_email_confirmation'
    return mocker.patch(mockname, return_value=None)


@pytest.fixture
def fake_photo(request, fs):
    fs.create_file('/test.jpg', contents=test_data.TEST_FILE)
    file = open('/test.jpg', 'rb')
    request.addfinalizer(file.close)
    return file


@pytest.fixture
def mock_tomorrow(mocker):
    today = timezone.now()
    tomorrow = today + datetime.timedelta(days=1)
    fixture = mocker.patch('django.utils.timezone.now', new=lambda: tomorrow)
    return fixture()


@pytest.fixture
def mock_yesterday(mocker):
    today = timezone.now()
    tomorrow = today - datetime.timedelta(days=1)
    fixture = mocker.patch('django.utils.timezone.now', new=lambda: tomorrow)
    return fixture()


@pytest.fixture
def candidate_statuses(anonym_client):
    resp = api_requests.get_candidate_statuses(anonym_client)
    assert resp.status_code == http.HTTPStatus.OK
    return resp.json()


@pytest.fixture
def cand_status_rejected(candidate_statuses):
    return next(i for i in candidate_statuses
                if i['name'] == constants.CANDIDATE_STATUS_REJECTED)


@pytest.fixture
def cand_status_applied(candidate_statuses):
    return next(i for i in candidate_statuses
                if i['name'] == constants.CANDIDATE_STATUS_APPLIED)


@pytest.fixture
def cand_status_screened(candidate_statuses):
    return next(i for i in candidate_statuses
                if i['name'] == constants.CANDIDATE_STATUS_SCREENED)


@pytest.fixture
def mock_has_subscription(mocker):
    mockname = 'permission.permissions.HasSubscription.has_permission'
    fixture = mocker.patch(mockname, return_value=True)
    return fixture()


@pytest.fixture
def industries(anonym_client):
    resp = api_requests.get_industries(anonym_client)
    assert resp.status_code == http.HTTPStatus.OK
    return resp.json()


@pytest.fixture
def event_types(company_user_client):
    resp = api_requests.get_event_types(company_user_client)
    assert resp.status_code == http.HTTPStatus.OK
    return resp.json()


@pytest.fixture
def event_interview(event_types):
    return next(
        i for i in event_types
        if i['name'] == constants.EVENT_TYPES_INTERVIEW_NAME
    )


@pytest.fixture
def event_screening(event_types):
    return next(
        i for i in event_types
        if i['name'] == constants.EVENT_TYPES_SCREENING_NAME
    )
