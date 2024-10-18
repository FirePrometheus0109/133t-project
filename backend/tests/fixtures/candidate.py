import datetime
import http

import mock
import pytest

from leet import constants
from leet import enums
from leet import models
from tests import api_requests
from tests import factories
from tests.api.candidate import constants as ct_constants

TOLTAL_CANDIDATES = 120
GROUP_CANDIDATE_WORKFLOW_STEPS_COUNT = 20  # candidates for each status
INITIAL_TIME_DELTA = 1


@pytest.fixture
def candidate(company_user_client, apply):
    resp = api_requests.get_candidates(company_user_client)
    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json()['count'] != 0
    return resp.json()['results'][0]


@pytest.fixture
def assigned_candidate(
        company_user_client, job1, job_seeker, purchased_job_seeker):
    data = {
        'jobs': [job1['id']],
        'job_seekers': [job_seeker.id]
    }
    resp = api_requests.assign_candidate_to_job(company_user_client, data)
    assert resp.status_code == http.HTTPStatus.CREATED
    resp = api_requests.get_candidates(company_user_client)
    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json()['count'] != 0
    return resp.json()['results'][0]


@pytest.fixture
def reapplied_candidate(
        mock_yesterday, candidate, mock_tomorrow, job_seeker_client):
    resp = api_requests.reapply_for_job(
        job_seeker_client,
        candidate['job']['id'])
    assert resp.status_code == http.HTTPStatus.OK
    return resp.json()


@pytest.fixture
def rejected_candidate(company_user_client, candidate, cand_status_rejected):
    data = {'status': cand_status_rejected['id']}
    resp = api_requests.update_candidate_status(
        company_user_client,
        candidate['id'],
        data)
    assert resp.status_code == http.HTTPStatus.OK
    return candidate


@pytest.fixture
def candidate_a_apply(company_user_client, started_autoapply):
    resp = api_requests.get_candidates(company_user_client)
    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json()['count'] != 0
    return resp.json()['results'][0]


@pytest.fixture
def candidate_a_apply_rejected(
        company_user_client, candidate_a_apply, cand_status_rejected):
    data = {'status': cand_status_rejected['id']}
    resp = api_requests.update_candidate_status(
        company_user_client,
        candidate_a_apply['id'],
        data)
    assert resp.status_code == http.HTTPStatus.OK
    return candidate_a_apply


@pytest.fixture
def company_candidates_workflow_stats(company_user, job_obj):
    """
    Essentially this fixture generate a bunch of candidates and guide them
    through candidates workflow steps with mocked date.
    """
    def create_candidate_workflow_step(cand, stat):
        time_delta_days = INITIAL_TIME_DELTA
        for i in range(GROUP_CANDIDATE_WORKFLOW_STEPS_COUNT):
            with mock.patch(
                    'django.utils.timezone.now',
                    new=lambda: ct_constants.FROM_DATE + datetime.timedelta(
                        days=time_delta_days)):
                wfs = factories.create_workflow_step(
                    candidate=cand,
                    status=stat,
                    owner=company_user)
                workflow_steps.append(wfs)
            # spread workflow steps for `basis` tests
            count = 1 if i % 2 else 2
            time_delta_days += count

    workflow_steps = []

    with mock.patch('django.utils.timezone.now',
                    new=lambda: ct_constants.FROM_DATE):
        candidates = []
        for _ in range(TOLTAL_CANDIDATES):
            js = factories.create_job_seeker()
            candidate = factories.create_candidate(
                job_seeker=js,
                company_user=company_user,
                job=job_obj)
            candidates.append(candidate)

        for status in constants.CANDIDATE_STATUSES:
            # skip `applied` status since candidates receive it on init
            if status != constants.CANDIDATE_STATUS_APPLIED:
                create_candidate_workflow_step(
                    cand=candidates.pop(),
                    stat=models.CandidateStatus.objects.get(name=status))
    return workflow_steps


@pytest.fixture
def candidate_good_rate(company_user_client, candidate):
    data = {'rating': enums.RatingEnum.GOOD.name}
    resp = api_requests.change_candidate_rating(
        company_user_client,
        candidate['id'],
        data)
    assert resp.status_code == http.HTTPStatus.OK
    return candidate


@pytest.fixture
def candidate_no_rate(company_user_client, candidate):
    data = {'rating': enums.RatingEnum.NO_RATING.name}
    resp = api_requests.change_candidate_rating(
        company_user_client,
        candidate['id'],
        data)
    assert resp.status_code == http.HTTPStatus.OK
    return candidate
