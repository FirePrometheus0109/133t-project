import datetime
import http

import pytest
from mock import mock

from candidate import constants
from leet import constants as leet_constants
from leet import enums
from leet import models
from tests import api_requests
from tests import factories
from tests.api.candidate import constants as ct_constants


@pytest.fixture
def assigned_candidates(
        company_user_client, company_jobs, job_seeker, purchased_job_seekers):
    data = {
        'jobs': [j['id'] for j in company_jobs],
        'job_seekers': [job_seeker.id]
    }
    resp = api_requests.assign_candidate_to_job(company_user_client, data)
    assert resp.status_code == http.HTTPStatus.CREATED

    resp = api_requests.get_candidates(company_user_client)
    assert resp.status_code == http.HTTPStatus.OK
    return resp.json()


@pytest.fixture
def apply_with_disqualifying_questionnaire(
        job_seeker_client, job_with_questions, answers_base_data):
    disqualifying_answers = answers_base_data.copy()
    disqualifying_answers[0]['answer']['yes_no_value'] = enums.YesNoAnswerEnum.YES.name
    resp = api_requests.create_answers_to_questions(
            job_seeker_client,
            job_with_questions['id'],
            disqualifying_answers)
    assert resp.status_code == http.HTTPStatus.CREATED
    resp = api_requests.apply_to_job(
        job_seeker_client,
        data={'job': job_with_questions['id']})
    assert resp.status_code == http.HTTPStatus.CREATED
    assert resp.json()['status'] == enums.ApplyStatusEnum.APPLIED.name


@pytest.fixture
def many_jobs(company_user_client_without_subscription, job_base_data,
              subscription_with_75_jobs):
    jobs = []
    for _ in range(constants.MAX_COUNT_OF_JOBS):
        resp = api_requests.create_job(
            company_user_client_without_subscription, job_base_data)
        assert resp.status_code == http.HTTPStatus.CREATED
        jobs.append(resp.json())
    return jobs


@pytest.fixture
def many_job_seekers():
    job_seekers = []
    for i in range(constants.MAX_COUNT_OF_JOB_SEEKERS):
        email = '{}uniqueemail@mail.com'.format(i)
        user = factories.auth.create_base_user(email=email)
        js = factories.auth.create_job_seeker(user=user)
        job_seekers.append(js)
    return job_seekers


@pytest.fixture
def company_user_candidate_1(company_user):
    return factories.candidate.create_candidate(company_user=company_user)


@pytest.fixture
def company_user_candidate_2(company_user):
    return factories.candidate.create_candidate(company_user=company_user)


@pytest.fixture
def company_user_candidates(company_user_candidate_1,
                            company_user_candidate_2):
    return [company_user_candidate_1, company_user_candidate_2]


@pytest.fixture
def candidates(company_user_client, job_seeker_client,
               job_seeker_2_client, job_seeker, job1, job2,
               purchased_job_seekers, job_seeker_2):
    # candidate with Django skill and from NY city
    resp = api_requests.assign_candidate_to_job(
        company_user_client, data={
            'jobs': [job1['id']],
            'job_seekers': [job_seeker.id]
        }
    )
    assert resp.status_code == http.HTTPStatus.CREATED
    # candidate from Ashville
    resp = api_requests.assign_candidate_to_job(
        company_user_client, data={
            'jobs': [job1['id']],
            'job_seekers': [job_seeker_2.id]
        }
    )
    assert resp.status_code == http.HTTPStatus.CREATED


@pytest.fixture
def job1_candidates(
        company_user_client, job_seeker, job_seeker_2,
        purchased_job_seekers, job1):
    data = {
        'jobs': [job1['id']],
        'job_seekers': [job_seeker.id, job_seeker_2.id]
    }
    resp = api_requests.assign_candidate_to_job(company_user_client, data)
    assert resp.status_code == http.HTTPStatus.CREATED
    resp = api_requests.get_candidates(company_user_client)
    assert resp.status_code == http.HTTPStatus.OK
    return resp.json()


@pytest.fixture
def candidate_status_data(cand_status_screened):
    return {
        'status': cand_status_screened['id']
    }


@pytest.fixture
def candidate_completed(
        company_user_client, candidate, candidate_statuses):
    # candidate with all steps exclude rejected
    for i in candidate_statuses:
        if i['name'] != leet_constants.CANDIDATE_STATUS_REJECTED:
            resp = api_requests.update_candidate_status(
                company_user_client,
                candidate['id'],
                {'status': i['id']})
            assert resp.status_code == http.HTTPStatus.OK
    resp = api_requests.get_candidates(company_user_client)
    assert resp.status_code == http.HTTPStatus.OK
    return next(i for i in resp.json()['results']
                if i['id'] == candidate['id'])


@pytest.fixture
def candidate_completed_rejected(
        company_user_client, candidate_completed, cand_status_rejected):
    resp = api_requests.update_candidate_status(
        company_user_client,
        candidate_completed['id'],
        {'status': cand_status_rejected['id']})
    assert resp.status_code == http.HTTPStatus.OK
    resp = api_requests.get_candidates(company_user_client)
    assert resp.status_code == http.HTTPStatus.OK
    return next(i for i in resp.json()['results']
                if i['id'] == candidate_completed['id'])

@pytest.fixture
def job_with_ans_survey(
        job_with_questions, job_seeker_client,
        answers_base_data):
    resp = api_requests.create_answers_to_questions(
        job_seeker_client,
        job_with_questions['id'],
        answers_base_data)
    assert resp.status_code == http.HTTPStatus.CREATED
    return job_with_questions


@pytest.fixture
def candidate_workflow_steps(company_user, job_seeker, job_obj):

    def update_candidate_workflow(timedelta_offset, status_name, candidate):
        timedelta = ct_constants.FROM_DATE - datetime.timedelta(
            days=timedelta_offset)
        status = models.CandidateStatus.objects.get(name=status_name)
        with mock.patch('django.utils.timezone.now', new=lambda: timedelta):
            factories.create_workflow_step(
                candidate=candidate,
                status=status)

    js = factories.create_job_seeker()
    candidate = factories.create_candidate(
        job_seeker=js,
        company_user=company_user,
        job=job_obj)

    update_candidate_workflow(
        60,
        leet_constants.CANDIDATE_STATUS_SCREENED,
        candidate)
    update_candidate_workflow(
        30,
        leet_constants.CANDIDATE_STATUS_OFFERED,
        candidate)
    update_candidate_workflow(
        13,
        leet_constants.CANDIDATE_STATUS_HIRED,
        candidate)


@pytest.fixture
def candidate_screened(company_user_client, candidate, cand_status_screened):
    data = {'status': cand_status_screened['id']}
    resp = api_requests.update_candidate_status(
        company_user_client,
        candidate['id'],
        data)
    assert resp.status_code == http.HTTPStatus.OK
    return candidate


@pytest.fixture
def candidate_viewed_details(company_user_client, candidate):
    resp = api_requests.get_candidate(company_user_client, candidate['id'])
    assert resp.status_code == http.HTTPStatus.OK
    return candidate


@pytest.fixture
def candidate_viewed_js_profile(company_user_client, candidate):
    resp = api_requests.get_job_seeker_details(
        company_user_client,
        candidate['job_seeker']['id'])
    assert resp.status_code == http.HTTPStatus.OK
    return candidate


@pytest.fixture
def candidate_viewed_quick_list(company_user_client, candidate):
    resp = api_requests.get_candidate_quick_view(company_user_client)
    assert resp.status_code == http.HTTPStatus.OK
    return candidate


@pytest.fixture
def candidate_commented(company_user_client, candidate):
    data = {
        'source': candidate['job_seeker']['id'],
        'title': 'title',
        'comment': 'comment'
    }
    resp = api_requests.create_job_seeker_comment(
        company_user_client,
        data)
    assert resp.status_code == http.HTTPStatus.CREATED
    return candidate
